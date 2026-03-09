#!/usr/bin/env python3
"""
Kundelead - Kundeanalyse og eierskapsverktøy
============================================
Samler informasjon om personer og selskaper fra offentlige registre
for å kartlegge eierskap, eiendommer og forretningsrelasjoner.

Kilder:
- Brønnøysundregisteret API (gratis)
- Proff.no aksjonærregister (web scraping)
- Kartverket/OpenStreetMap (geocoding)

Bruk:
    from kundelead import Kundelead

    p = Kundelead()
    resultat = p.analyser_person("Ola Nordmann")
    resultat = p.analyser_selskap("123456789")
    p.generer_rapport(resultat, "rapport.md")
    p.generer_kart(resultat, "kart.html")
"""

import requests
import re
import time
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from urllib.parse import quote
from pathlib import Path

# Valgfrie avhengigheter
try:
    import folium
    from folium.plugins import MarkerCluster
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Selskap:
    """Representerer et selskap"""
    orgnr: str
    navn: str
    bransje: Optional[str] = None
    formaal: Optional[str] = None
    adresse: Optional[str] = None
    kommune: Optional[str] = None
    fylke: Optional[str] = None
    stiftet: Optional[str] = None
    hjemmeside: Optional[str] = None
    ansatte: Optional[int] = None
    sum_eiendeler: Optional[float] = None


@dataclass
class Eierskap:
    """Representerer et eierforhold"""
    eier_orgnr: Optional[str]
    eier_navn: str
    selskap_orgnr: str
    selskap_navn: str
    andel_prosent: float
    via_selskap: Optional[str] = None  # For indirekte eierskap


@dataclass
class Eiendom:
    """Representerer en eiendom"""
    navn: str
    adresse: str
    kommune: str
    fylke: str
    type: str
    selskap_orgnr: str
    selskap_navn: str
    eierandel: float
    eierstruktur: str  # "direkte" eller "via X"
    lat: Optional[float] = None
    lng: Optional[float] = None
    verdi: Optional[float] = None


@dataclass
class Person:
    """Representerer en person"""
    navn: str
    fodselsaar: Optional[int] = None
    adresse: Optional[str] = None
    roller: List[Dict] = field(default_factory=list)
    eierskap: List[Eierskap] = field(default_factory=list)


@dataclass
class KundeleadResultat:
    """Samlet resultat fra kundeleadanalyse"""
    target_navn: str
    target_type: str  # "person" eller "selskap"
    selskaper: Dict[str, Selskap] = field(default_factory=dict)
    eierskap: List[Eierskap] = field(default_factory=list)
    eiendommer: List[Eiendom] = field(default_factory=list)
    roller: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# BRØNNØYSUNDREGISTERET API
# ============================================================================

class BrregAPI:
    """Klient for Brønnøysundregisteret Enhetsregisteret API"""

    BASE_URL = "https://data.brreg.no/enhetsregisteret/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Kundelead/1.0 (kundeanalyse)'
        })

    def hent_enhet(self, orgnr: str) -> Optional[dict]:
        """Hent info om en enhet fra organisasjonsnummer"""
        orgnr = orgnr.replace(" ", "")
        url = f"{self.BASE_URL}/enheter/{orgnr}"
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                # Prøv underenheter
                url = f"{self.BASE_URL}/underenheter/{orgnr}"
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    return resp.json()
        except Exception as e:
            print(f"  Feil ved henting av {orgnr}: {e}")
        return None

    def sok_enheter(self, navn: str, size: int = 20) -> List[dict]:
        """Søk etter enheter på navn"""
        url = f"{self.BASE_URL}/enheter"
        params = {'navn': navn, 'size': size}
        try:
            resp = self.session.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('_embedded', {}).get('enheter', [])
        except Exception as e:
            print(f"  Feil ved søk: {e}")
        return []

    def hent_roller(self, orgnr: str) -> Optional[dict]:
        """Hent rolleinfo for en enhet"""
        orgnr = orgnr.replace(" ", "")
        url = f"{self.BASE_URL}/enheter/{orgnr}/roller"
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None

    def parse_selskap(self, data: dict) -> Selskap:
        """Parse API-respons til Selskap-objekt"""
        adresse_data = data.get('forretningsadresse', {}) or data.get('beliggenhetsadresse', {})
        adresse_deler = adresse_data.get('adresse', [])
        adresse = ', '.join(adresse_deler) if adresse_deler else None
        if adresse and adresse_data.get('postnummer'):
            adresse += f", {adresse_data.get('postnummer')} {adresse_data.get('poststed', '')}"

        naeringskode = data.get('naeringskode1', {})
        formaal_liste = data.get('vedtektsfestetFormaal', [])

        return Selskap(
            orgnr=data.get('organisasjonsnummer', ''),
            navn=data.get('navn', ''),
            bransje=naeringskode.get('beskrivelse') if naeringskode else None,
            formaal=' '.join(formaal_liste) if formaal_liste else None,
            adresse=adresse,
            kommune=adresse_data.get('kommune'),
            stiftet=data.get('stiftelsesdato'),
            hjemmeside=data.get('hjemmeside'),
            ansatte=data.get('antallAnsatte')
        )


# ============================================================================
# PROFF.NO SCRAPER
# ============================================================================

class ProffScraper:
    """Scraper for Proff.no aksjonærdata"""

    BASE_URL = "https://www.proff.no"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'no,en;q=0.5',
        })

    def hent_selskapsside(self, orgnr: str) -> Optional[str]:
        """Hent HTML for selskapssiden"""
        url = f"{self.BASE_URL}/aksjonærer/bedrift/-/{orgnr}"
        try:
            resp = self.session.get(url, timeout=15)
            time.sleep(0.5)  # Rate limiting
            if resp.status_code == 200:
                return resp.text
        except Exception as e:
            print(f"  Feil ved scraping av {orgnr}: {e}")
        return None

    def sok_person(self, navn: str) -> List[dict]:
        """Søk etter person i aksjonærregisteret"""
        encoded_navn = quote(navn)
        url = f"{self.BASE_URL}/søk-etter-aksjonær?q={encoded_navn}"
        resultater = []

        try:
            resp = self.session.get(url, timeout=15)
            time.sleep(0.5)
            if resp.status_code == 200:
                html = resp.text
                # Finn personer med aksjonærprofil-lenker
                pattern = r'/aksjonærer/person/([^/]+)/(\d+)'
                matches = re.findall(pattern, html)
                seen = set()
                for navn_slug, person_id in matches[:10]:
                    if person_id not in seen:
                        seen.add(person_id)
                        resultater.append({
                            'navn': navn_slug.replace('-', ' ').title(),
                            'proff_id': person_id,
                            'url': f"{self.BASE_URL}/aksjonærer/person/{navn_slug}/{person_id}"
                        })
        except Exception as e:
            print(f"  Feil ved personsøk: {e}")

        return resultater

    def hent_personside(self, proff_url: str) -> Optional[str]:
        """Hent HTML for personsiden"""
        try:
            resp = self.session.get(proff_url, timeout=15)
            time.sleep(0.5)
            if resp.status_code == 200:
                return resp.text
        except Exception:
            pass
        return None

    def parse_eierskap_fra_html(self, html: str, context_orgnr: str = None) -> List[dict]:
        """Ekstraher eierskapsinfo fra Proff HTML"""
        eierskap = []

        # Finn alle orgnr og andeler
        # Pattern: orgnr (9 siffer) etterfulgt av andel (X,XX%)
        orgnr_pattern = r'(\d{9})'
        andel_pattern = r'(\d+(?:,\d+)?)\s*%'

        orgnr_matches = re.findall(orgnr_pattern, html)
        andel_matches = re.findall(andel_pattern, html)

        # Enkel matching (forbedres med BeautifulSoup for produksjon)
        for i, orgnr in enumerate(orgnr_matches[:len(andel_matches)]):
            if orgnr != context_orgnr:
                andel = float(andel_matches[i].replace(',', '.')) if i < len(andel_matches) else 0
                if andel > 0:
                    eierskap.append({
                        'orgnr': orgnr,
                        'andel': andel
                    })

        return eierskap


# ============================================================================
# GEOCODING
# ============================================================================

# Kjente koordinater (backup)
KNOWN_COORDINATES = {
    "Oslo": (59.9139, 10.7522),
    "Bergen": (60.3913, 5.3221),
    "Trondheim": (63.4305, 10.3951),
    "Stavanger": (58.9700, 5.7331),
    "Kristiansand": (58.1599, 8.0182),
    "Evje": (58.5760, 7.8440),
    "Sandnes": (58.8527, 5.7328),
}


def geocode_adresse(adresse: str) -> Optional[tuple]:
    """Konverter adresse til koordinater"""
    if not adresse:
        return None

    # Sjekk kjente koordinater først (kommune/by)
    for sted, coords in KNOWN_COORDINATES.items():
        if sted.lower() in adresse.lower():
            return coords

    if not GEOPY_AVAILABLE:
        return None

    try:
        geolocator = Nominatim(user_agent="kundelead_kundeanalyse")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(f"{adresse}, Norge")
        if location:
            return (location.latitude, location.longitude)
    except Exception:
        pass

    return None


# ============================================================================
# HOVEDKLASSE: KUNDELEAD
# ============================================================================

class Kundelead:
    """Hovedklasse for kundeanalyse og kundeleadering"""

    def __init__(self, verbose: bool = True):
        self.brreg = BrregAPI()
        self.proff = ProffScraper()
        self.verbose = verbose
        self._cache = {}

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def analyser_person(self, navn: str, max_dybde: int = 2) -> KundeleadResultat:
        """Analyser eierskap og roller for en person"""
        self._log(f"\n{'='*60}")
        self._log(f"KUNDELEADANALYSE: {navn}")
        self._log(f"{'='*60}\n")

        resultat = KundeleadResultat(
            target_navn=navn,
            target_type="person",
            metadata={'analysert': time.strftime('%Y-%m-%d %H:%M')}
        )

        # Søk etter personen i Proff
        self._log("Søker i aksjonærregisteret...")
        treff = self.proff.sok_person(navn)

        if not treff:
            self._log(f"  Ingen treff for '{navn}'")
            return resultat

        self._log(f"  Fant {len(treff)} treff")

        # Analyser første treff (eller be bruker velge)
        person_info = treff[0]
        self._log(f"  Analyserer: {person_info['navn']}")

        # Hent personside
        html = self.proff.hent_personside(person_info['url'])
        if html:
            # Parse roller og eierskap
            self._parse_persondata(html, resultat)

        # Analyser hvert selskap personen er involvert i
        for eierskap in resultat.eierskap:
            self._analyser_selskap_rekursivt(
                eierskap.selskap_orgnr,
                resultat,
                dybde=0,
                max_dybde=max_dybde
            )

        # Finn eiendommer
        self._identifiser_eiendommer(resultat)

        return resultat

    def analyser_selskap(self, orgnr: str, max_dybde: int = 2) -> KundeleadResultat:
        """Analyser et selskap og dets eierstruktur"""
        orgnr = orgnr.replace(" ", "")

        self._log(f"\n{'='*60}")
        self._log(f"SELSKAPSANALYSE: {orgnr}")
        self._log(f"{'='*60}\n")

        resultat = KundeleadResultat(
            target_navn=orgnr,
            target_type="selskap",
            metadata={'analysert': time.strftime('%Y-%m-%d %H:%M')}
        )

        self._analyser_selskap_rekursivt(orgnr, resultat, dybde=0, max_dybde=max_dybde)
        self._identifiser_eiendommer(resultat)

        return resultat

    def _analyser_selskap_rekursivt(self, orgnr: str, resultat: KundeleadResultat,
                                     dybde: int, max_dybde: int):
        """Rekursiv analyse av selskapsstruktur"""
        if dybde > max_dybde or orgnr in resultat.selskaper:
            return

        indent = "  " * dybde
        self._log(f"{indent}Analyserer selskap {orgnr}...")

        # Hent fra Brønnøysund
        data = self.brreg.hent_enhet(orgnr)
        if not data:
            return

        selskap = self.brreg.parse_selskap(data)
        resultat.selskaper[orgnr] = selskap

        if dybde == 0:
            resultat.target_navn = selskap.navn

        self._log(f"{indent}  {selskap.navn}")
        if selskap.bransje:
            self._log(f"{indent}    Bransje: {selskap.bransje}")

        # Hent eierskap fra Proff
        html = self.proff.hent_selskapsside(orgnr)
        if html:
            eierskap_data = self.proff.parse_eierskap_fra_html(html, orgnr)
            for e in eierskap_data:
                resultat.eierskap.append(Eierskap(
                    eier_orgnr=e['orgnr'],
                    eier_navn="",  # Hentes senere
                    selskap_orgnr=orgnr,
                    selskap_navn=selskap.navn,
                    andel_prosent=e['andel']
                ))

        # Hent roller
        roller_data = self.brreg.hent_roller(orgnr)
        if roller_data:
            for rolle in roller_data.get('rollegrupper', []):
                for r in rolle.get('roller', []):
                    resultat.roller.append({
                        'selskap': selskap.navn,
                        'orgnr': orgnr,
                        'rolle': rolle.get('type', {}).get('beskrivelse', ''),
                        'person': r.get('person', {}).get('navn', {}).get('fornavn', '') + ' ' +
                                  r.get('person', {}).get('navn', {}).get('etternavn', '')
                    })

    def _parse_persondata(self, html: str, resultat: KundeleadResultat):
        """Parse persondata fra Proff HTML"""
        # Finn selskaper personen eier aksjer i
        orgnr_pattern = r'/aksjonærer/bedrift/[^/]+/(\d{9})'
        matches = re.findall(orgnr_pattern, html)

        for orgnr in set(matches):
            resultat.eierskap.append(Eierskap(
                eier_orgnr=None,
                eier_navn=resultat.target_navn,
                selskap_orgnr=orgnr,
                selskap_navn="",  # Hentes senere
                andel_prosent=0  # Hentes senere
            ))

    def _identifiser_eiendommer(self, resultat: KundeleadResultat):
        """Identifiser eiendommer basert på selskapsdata"""
        eiendomsnøkkelord = [
            'eiendom', 'bolig', 'utleie', 'bygning', 'tomt',
            'kjøpesenter', 'hotell', 'hyttefelt', 'fjellstue'
        ]

        for orgnr, selskap in resultat.selskaper.items():
            er_eiendom = False

            # Sjekk bransje/formål
            tekst = f"{selskap.bransje or ''} {selskap.formaal or ''}".lower()
            for nøkkelord in eiendomsnøkkelord:
                if nøkkelord in tekst:
                    er_eiendom = True
                    break

            if er_eiendom and selskap.adresse:
                # Finn eierandel
                andel = 100.0
                for e in resultat.eierskap:
                    if e.selskap_orgnr == orgnr:
                        andel = e.andel_prosent
                        break

                coords = geocode_adresse(selskap.adresse)

                resultat.eiendommer.append(Eiendom(
                    navn=selskap.navn,
                    adresse=selskap.adresse,
                    kommune=selskap.kommune or "",
                    fylke="",
                    type=selskap.bransje or "Eiendom",
                    selskap_orgnr=orgnr,
                    selskap_navn=selskap.navn,
                    eierandel=andel,
                    eierstruktur="direkte" if andel == 100 else f"{andel}%",
                    lat=coords[0] if coords else None,
                    lng=coords[1] if coords else None,
                    verdi=selskap.sum_eiendeler
                ))

    # ========================================================================
    # RAPPORTGENERERING
    # ========================================================================

    def generer_rapport(self, resultat: KundeleadResultat, output_fil: str = None) -> str:
        """Generer markdown-rapport etter Nivåmetoden"""

        rapport = []
        rapport.append(f"# Kundeleadanalyse: {resultat.target_navn}\n")

        # HOVEDBUDSKAP
        rapport.append("## HOVEDBUDSKAP\n")
        antall_selskaper = len(resultat.selskaper)
        antall_eiendommer = len(resultat.eiendommer)
        rapport.append(
            f"{resultat.target_navn} er involvert i {antall_selskaper} selskaper "
            f"med {antall_eiendommer} identifiserte eiendommer. "
            f"Analysen viser eierstruktur og geografisk fordeling.\n"
        )

        rapport.append("---\n")

        # ARGUMENTASJON
        rapport.append("## ARGUMENTASJON\n")

        # 1. Selskaper
        rapport.append("### 1. Selskapsoversikt\n")
        rapport.append("| Selskap | Org.nr | Bransje | Adresse |")
        rapport.append("|---------|--------|---------|---------|")
        for orgnr, s in resultat.selskaper.items():
            rapport.append(f"| {s.navn} | {orgnr} | {s.bransje or '-'} | {s.adresse or '-'} |")
        rapport.append("")

        # 2. Eiendommer
        if resultat.eiendommer:
            rapport.append("### 2. Eiendommer\n")
            rapport.append("| Eiendom | Kommune | Type | Eierandel |")
            rapport.append("|---------|---------|------|-----------|")
            for e in resultat.eiendommer:
                rapport.append(f"| {e.navn} | {e.kommune} | {e.type} | {e.eierstruktur} |")
            rapport.append("")

        # 3. Roller
        if resultat.roller:
            rapport.append("### 3. Roller\n")
            rapport.append("| Selskap | Rolle | Person |")
            rapport.append("|---------|-------|--------|")
            for r in resultat.roller[:20]:  # Begrens til 20
                rapport.append(f"| {r['selskap']} | {r['rolle']} | {r['person']} |")
            rapport.append("")

        rapport.append("---\n")

        # BEVISFØRING
        rapport.append("## BEVISFØRING\n")
        rapport.append(f"*Rapport generert: {resultat.metadata.get('analysert', 'N/A')}*\n")
        rapport.append("*Kilder: Brønnøysundregisteret, Proff.no*\n")

        rapport_tekst = "\n".join(rapport)

        if output_fil:
            Path(output_fil).write_text(rapport_tekst, encoding='utf-8')
            self._log(f"\nRapport lagret: {output_fil}")

        return rapport_tekst

    def generer_kart(self, resultat: KundeleadResultat, output_fil: str = "kundelead_kart.html") -> Optional[str]:
        """Generer interaktivt kart med eiendommer"""

        if not FOLIUM_AVAILABLE:
            self._log("Folium ikke installert. Kan ikke generere kart.")
            return None

        if not resultat.eiendommer:
            self._log("Ingen eiendommer å vise på kart.")
            return None

        # Finn senterpunkt
        lats = [e.lat for e in resultat.eiendommer if e.lat]
        lngs = [e.lng for e in resultat.eiendommer if e.lng]

        if not lats:
            center = [59.9, 10.7]  # Default: Oslo
        else:
            center = [sum(lats)/len(lats), sum(lngs)/len(lngs)]

        m = folium.Map(location=center, zoom_start=7, tiles='OpenStreetMap')

        for e in resultat.eiendommer:
            if e.lat and e.lng:
                popup_html = f"""
                <b>{e.navn}</b><br>
                Adresse: {e.adresse}<br>
                Type: {e.type}<br>
                Eierandel: {e.eierstruktur}
                """
                folium.Marker(
                    location=[e.lat, e.lng],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=e.navn,
                    icon=folium.Icon(color='blue', icon='home', prefix='fa')
                ).add_to(m)

        m.save(output_fil)
        self._log(f"\nKart lagret: {output_fil}")
        return output_fil

    def eksporter_json(self, resultat: KundeleadResultat, output_fil: str) -> str:
        """Eksporter resultat som JSON"""
        data = {
            'target': resultat.target_navn,
            'type': resultat.target_type,
            'metadata': resultat.metadata,
            'selskaper': {k: asdict(v) for k, v in resultat.selskaper.items()},
            'eierskap': [asdict(e) for e in resultat.eierskap],
            'eiendommer': [asdict(e) for e in resultat.eiendommer],
            'roller': resultat.roller
        }

        Path(output_fil).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        self._log(f"\nJSON eksportert: {output_fil}")
        return output_fil


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Kundelead - Kundeanalyse og eierskapsverktøy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eksempler:
  python kundelead.py --person "Ola Nordmann"
  python kundelead.py --selskap 988177091
  python kundelead.py --selskap 988177091 --rapport rapport.md --kart kart.html
        """
    )

    parser.add_argument('--person', help='Analyser person')
    parser.add_argument('--selskap', help='Analyser selskap (orgnr)')
    parser.add_argument('--rapport', help='Lagre rapport (markdown)')
    parser.add_argument('--kart', help='Generer kart (HTML)')
    parser.add_argument('--json', help='Eksporter som JSON')
    parser.add_argument('--dybde', type=int, default=2, help='Analysedybde (default: 2)')
    parser.add_argument('--stille', action='store_true', help='Minimal output')

    args = parser.parse_args()

    if not args.person and not args.selskap:
        parser.print_help()
        return

    p = Kundelead(verbose=not args.stille)

    if args.person:
        resultat = p.analyser_person(args.person, max_dybde=args.dybde)
    else:
        resultat = p.analyser_selskap(args.selskap, max_dybde=args.dybde)

    if args.rapport:
        p.generer_rapport(resultat, args.rapport)
    else:
        print(p.generer_rapport(resultat))

    if args.kart:
        p.generer_kart(resultat, args.kart)

    if args.json:
        p.eksporter_json(resultat, args.json)


if __name__ == "__main__":
    main()
