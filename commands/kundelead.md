---
name: kundelead
description: "Analyser potensielle kunder - kartlegg eierskap, eiendommer og forretningsrelasjoner"
category: business-intelligence
complexity: standard
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - WebFetch
---

# /kc:kundelead - Kundeanalyse og Prospektering

> **KC Framework**: Samle og analysere informasjon om potensielle kunder fra offentlige registre.

## Bruk
```
/kc:kundelead "Navn på person"
/kc:kundelead --orgnr 123456789
/kc:kundelead "Firmanavn AS"
```

## Hva den gjør

1. **Søker** i Brønnøysundregisteret og Proff.no
2. **Kartlegger** eierstruktur (direkte og indirekte)
3. **Finner** eiendommer og verdier
4. **Identifiserer** beslutningstakere og roller
5. **Genererer** rapport med Nivåmetoden-struktur
6. **Lager** interaktivt kart over eiendommer

## Eksempel output

```
KUNDEANALYSE: Terje Vasland
===========================

HOVEDBUDSKAP:
Terje Vasland kontrollerer 15 eiendommer gjennom TERVI AS,
med geografisk tyngdepunkt i Evje og Hornnes (60%).

ARGUMENTASJON:
1. Eierstruktur (organisasjonskart)
2. Eiendomsoversikt (tabell med 15 eiendommer)
3. Geografisk fordeling (kart)

BEVISFØRING:
- Vedlegg A: Selskapsdetaljer
- Vedlegg B: Eierandelsberegning
```

## Flagg

| Flagg | Beskrivelse |
|-------|-------------|
| `--orgnr` | Søk på organisasjonsnummer |
| `--dybde N` | Analysedybde (default: 2) |
| `--rapport fil.md` | Lagre rapport til fil |
| `--kart fil.html` | Generer interaktivt kart |
| `--docx` | Konverter til Word (bruker Norsk Solkraft-mal) |
| `--enok` | Bruk Norsk ENØK-mal for Word |

## Datakilder

- **Brønnøysundregisteret** (API): Selskapsinfo, stiftelsesdato, bransje, adresse
- **Proff.no** (scraping): Aksjonærer, eierskap, regnskapstall
- **OpenStreetMap** (Nominatim): Geocoding for kart

## Forretningsrelevans

Agenten vurderer automatisk:
- Solenergi-potensial for eiendommer
- ENØK-potensial for bygninger
- Beslutningstakere som bør kontaktes
- Porteføljestørrelse

## Python CLI

```bash
# Direkte bruk av Python-scriptet
python ~/klauspython/kc/scripts/kundelead.py --person "Ola Nordmann"
python ~/klauspython/kc/scripts/kundelead.py --selskap 988177091 --rapport rapport.md --kart kart.html
```

## Se også

- `/kc:nivametoden` - Rapportstrukturering
- `/kc:md2docx` - Word-konvertering

---

## Workflow (for agenten)

Når denne skillen aktiveres:

1. **Parse input**: Identifiser om det er person, selskap eller orgnr
2. **Kjør kundelead.py**: Samle data fra registre
3. **Analyser resultater**: Identifiser mønstre og forretningsmuligheter
4. **Generer rapport**: Bruk Nivåmetoden-struktur
5. **Lag kart**: Hvis eiendommer finnes
6. **Presenter resultater**: Oppsummer funn for brukeren

```bash
# Eksempel på intern kjøring
cd ~/klauspython/kc/scripts
python kundelead.py --person "$INPUT" --rapport /tmp/kundelead_rapport.md --kart /tmp/kundelead_kart.html --json /tmp/kundelead_data.json
```

Etter kjøring, les rapporten og presenter den til brukeren med eventuell tilleggsinnsikt.
