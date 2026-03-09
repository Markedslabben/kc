---
name: pv-diagnostics
description: "Systematisk diagnostisk analyse av Growatt solcelleanlegg med terminal-output og markdown-rapport"
category: pv-monitoring
complexity: advanced
---

# /kc:pv-diagnostics - PV Anleggsdiagnostikk

> Systematisk analyse av Growatt solcelleanlegg med hypotesetesting, MPPT-analyse og ytelsesberegning.
> Basert på IEA PVPS overvåkingsstandard og Norsk Solkraft beste praksis.

---

## Invokasjon

```
/kc:pv-diagnostics <anleggsnavn-eller-plant_id> [--deep] [--report]
```

**Eksempler:**
```
/kc:pv-diagnostics Helvik                  # Søk etter anlegg, kjør analyse
/kc:pv-diagnostics 2612769                 # Direkte med plant_id
/kc:pv-diagnostics Finsnes --deep          # Dyp analyse med flere historiske datoer
/kc:pv-diagnostics Helvik --report         # Generer full markdown-rapport
```

---

## Analyseprotokoll (7 faser)

### Fase 1: Identifikasjon og oppsett

**Mål**: Finn anlegget, identifiser invertere, etabler kontekst.

1. **Finn anlegget** i Growatt API:
   - Hvis `plant_id` gitt direkte → bruk den
   - Ellers: kjør `scripts/list_all_plants.py` og søk etter navn
   - Identifiser hvilken Growatt-konto (sirdal/kvinesdal/byrkjedal) anlegget tilhører

2. **Hent device-liste** via `/device/list?plant_id=X`:
   - Kartlegg alle invertere: SN, modell, datalogger
   - Merk type 1 (inverter) vs type 4 (datalogger)
   - Sjekk `lost` status og `last_update_time`

3. **Sjekk prosjektmappe** (om tilgjengelig):
   ```
   /mnt/c/Users/klaus/NorskSolkraft AS/Gruppeområde - Documents/10 Prosjekter/
   ```
   - Søk etter adresse/navn i 2024/ og 2025/
   - Se etter PVsol-fil, strengkonfigurasjon, kalkyle

4. **Etabler kontekst**:
   - Registrert kapasitet (kWp)
   - Geografisk plassering → forventet kWh/kWp/år (PVGIS)
   - Idriftsettelsesdato (fra Growatt eller prosjektmappe)
   - Antall invertere og MPPT-innganger

**Output**: Tabell med anleggsdata og inverteroversikt.

---

### Fase 2: Nåværende status

**Mål**: Er anlegget i drift? Produserer det nå?

For HVER inverter, hent `/device/inverter/last_new_data`:

1. **Online-status**:
   - `statusText`: Normal / Waiting / Fault
   - `time`: Siste kontakt (er den fersk?)
   - Vurder om "Waiting" er normalt (natt/skumring)

2. **Produksjon nå**:
   - `pac` (AC effekt, W)
   - `ppv` (DC effekt, W)
   - `powerToday` (kWh i dag)

3. **Nettparametre**:
   - `vacr/vacs/vact` (AC spenning per fase)
   - `fac` (frekvens, Hz) — sjekk om innenfor 49.8–50.2 Hz
   - `pf` (power factor)
   - **IT-nett sjekk**: Hvis vacr ≈ 130-138V → IT-nett (230V/√3), dette er normalt

4. **Alarmer og feil**:
   - `warnCode`: 0 = OK, >0 = advarsel (slå opp i Growatt-manual)
   - `faultCode1/2`: 0 = OK
   - `faultType`/`faultValue`

5. **Isolasjonsresistans**:
   - `pvIso`: > 1000 kΩ = bra, < 500 kΩ = undersøk, < 100 kΩ = kritisk

6. **MPPT-energibalanse** (KRITISK SJEKK):
   - For i=1..N: `epv{i}Total` (lifetime) og `epv{i}Today`
   - Beregn gjennomsnitt og avvik
   - **Flagg MPPT-er med <10% av gjennomsnitt som KRITISK**
   - Identifiser gruppering (noen MPPT-er har 2 strenger, andre 1)

7. **Strengovervåking** (hvis tilgjengelig):
   - `vString{n}` og `currentString{n}` i par per MPPT
   - Sammenlign parvis: store avvik mellom strenger = problem

8. **Tellerverifikasjon**:
   - `powerTotal` (AC kWh) vs `epvTotal` (DC kWh)
   - Ratio bør være 0.85-0.98 (invertortap)
   - Ratio > 1.0 = telleranomalitet
   - Ratio < 0.7 = usedvanlig høyt tap

**Output**: Status-tabell + MPPT-energioversikt + flaggede problemer.

---

### Fase 3: Historisk analyse

**Mål**: Er problemene nye eller har de eksistert lenge? Finne peak-produksjonsdata.

**VIKTIG**: Growatt historisk data returnerer ALLE 5-min intervaller for en dag (288 records).
Bruk `max(records, key=pac)` for å finne peak, men FILTRER først for pac > 0.

1. **Velg datoer** (spread over tid):
   - I dag / i går
   - 1 uke siden
   - 1 måned siden
   - 3 måneder siden (om tilgjengelig)

2. **For hver dato**, for HVER inverter:
   - Hent `/device/inverter/data?start_date=X&end_date=X&perpage=100`
   - **VIKTIG**: perpage maks 100 (API gir error_code 10013 ved >100)
   - **Filtrer til dagslysrecords** (pac > 0 ELLER ppv > 0)
   - Finn peak-record (høyeste pac)
   - Ved peak: noter vpv1..N, ipv1..N, ppv1..N
   - Beregn dagsproduksjon fra epvToday-verdier

3. **MPPT spenningssammenligning**:
   - Sammenlign vpv-verdier ved peak mellom invertere og over tid
   - Identifiser MPPT-er med konsekvent lavere spenning
   - Beregn ratio mot "frisk" referanse-MPPT
   - **Finsnes-metoden**: Bruk INV med alle normale MPPT som referanse

4. **Produksjonskurve** (for beste dag):
   - Vis timesbasert peak-effekt gjennom dagen
   - Sjekk for clipping (flat topp = inverter begrenser)
   - Sjekk for uventet dropp midt på dagen (skygge, feil)

**Output**: Historisk spenningstabell + avviksidentifikasjon.

**Rate limiting**: Growatt API har 5s+ delay mellom kall. Bruk `time.sleep(8)`.

---

### Fase 4: Alarmhistorikk

**Mål**: Finne gjentakende alarmer og mønster.

1. **Skann alarmer** for hver inverter:
   - Sjekk `/device/inverter/alarm?device_sn=X&date=Y&perpage=100`
   - Skann minst 1 dato per uke, 3 måneder tilbake
   - Grupper etter `alarm_code`

2. **Klassifiser alarmer**:
   | Kode-range | Type | Handling |
   |-----------|------|---------|
   | 100-199 | DC-feil (streng/panel) | Sjekk strenger |
   | 200-299 | DC-overspenning/underspenning | Sjekk strengkonfig |
   | 300-399 | AC-feil (nett) | Sjekk nettilkobling |
   | 400-499 | Temperatur/intern | Sjekk ventilasjon |
   | 500-699 | Isolasjon/jordfeil | Sjekk kabler/paneler |
   | 700-899 | Kommunikasjon | Sjekk datalogger |
   | 900+ | Firmware-spesifikk | Kontakt Growatt |

3. **Mønster-deteksjon**:
   - Samme alarm daglig = kronisk problem
   - Alarm kun på én inverter = inverter-spesifikt
   - Alarm korrelert med tidspunkt = mulig skygge/temperatur

**Output**: Alarmtabell med frekvens og klassifisering.

---

### Fase 5: Ytelsesberegning

**Mål**: Leverer anlegget som forventet?

1. **Spesifikk ytelse (kWh/kWp)**:
   - Lifetime: `sum(powerTotal) / kapasitet_kWp`
   - Annualisert: Juster for driftstid

2. **Referanseverdier** (Sør-Norge):
   | Breddegrad | Flat tak | 30° sør | Øst-vest |
   |-----------|---------|---------|----------|
   | 58-59°N | 750-850 | 850-950 | 800-900 |
   | 60-62°N | 700-800 | 800-900 | 750-850 |
   | 63-65°N | 650-750 | 750-850 | 700-800 |
   | 66-69°N | 550-700 | 650-800 | 600-750 |

3. **Performance Ratio estimat**:
   - PR = faktisk_kWh/kWp / forventet_kWh/kWp
   - God: > 80%, OK: 70-80%, Dårlig: < 70%

4. **Inverterbalanse**:
   - Sammenlign powerToday og powerTotal mellom invertere
   - Beregn prosentvis fordeling
   - Flagg ubalanse > 15% (justert for kapasitetsforskjell)

5. **Tapt energi** (for identifiserte feil):
   - Estimer kWh tapt pga. døde MPPT-er, nedetid, etc.
   - Beregn økonomisk tap (ca. 1 NOK/kWh spotpris)

**Output**: Ytelsessammendrag med flaggede avvik.

---

### Fase 6: Hypotesetesting

**Mål**: Oppnå høy konfidens på årsaksforklaring for hvert identifisert problem.

Ikke konkluder uten å ha testet hypotesene. Funn fra fase 1-5 er observasjoner —
hypotesetesting gjør dem til konklusjoner med konfidensnivå.

1. **Formuler hypoteser** for hvert problem:
   - Minst 2-4 konkurrerende hypoteser per problem
   - Hver hypotese skal ha testbare prediksjoner
   - Eksempel: "Hvis snø → korrelerer med temperatur, alle invertere påvirkes samtidig"

2. **Design tester** som kan falsifisere hypoteser:
   - Bruk data fra fase 2-5 som førstegangstest
   - Hent tilleggsdata ved behov (værdata, flere datoer, andre invertere)
   - Hver test skal kunne bekrefte ELLER falsifisere minst én hypotese

3. **Kjør tester parallelt** der mulig:
   - Temperaturkorrelasjon (Open-Meteo arkiv-API)
   - Irradianskorrelasjon (GHI vs. produksjon)
   - Inverterkorrelasjon (mister de MPPTs på samme dag?)
   - Spenningssignatur-analyse (bypass-dioder, snøklassifisering)

4. **Vurder resultater**:
   - Konfidensnivå per hypotese: Bekreftet / Svekket / Falsifisert
   - Minst én hypotese skal ha over 80% konfidens før konklusjon
   - Hvis ingen hypotese når 80%: formuler nye hypoteser (runde 2)

5. **Iterativ prosess**:
   - Runde 1: Grunnleggende korrelasjonstester
   - Runde 2: Dypere analyse basert på runde 1-funn
   - Runde 3: Spesialtester for gjenværende usikkerhet
   - Stopp når hovedhypotesene har tilstrekkelig konfidens

**Verktøy tilgjengelig for hypotesetesting**:
- `backend/snow_detection.py`: Snøklassifisering fra MPPT V/I-signaturer (5 modi)
- `backend/clearsky_detection.py`: Clearsky-indeks for å skille skyer fra snø
- `backend/weather_service.py`: CAMS/Open-Meteo værdata
- Open-Meteo arkiv-API: Historisk temperatur, GHI, snødybde, snøfall
- met.no locationforecast: Norsk temperatur- og nedbørprognose (bedre enn Open-Meteo for snø)

**Output**: Hypotesetabell med konfidensnivå + bevisgrunnlag for konklusjoner.

---

### Fase 7: Rapport og anbefalinger

**Mål**: Saml alt i oversiktlig rapport. Rett på sak — teknisk, konsist, datadrevet.

**RAPPORTFORMAT — NIVÅMETODEN**:
- Ingen emojis i rapporten. Bruk tekstetiketter (KRITISK, NORMAL, etc.)
- Ingen SCQA-rammeverk eller narrativ innramming — dette er en teknisk rapport
- Hovedbudskap FØRST (~100 ord): Hva er galt, hva er årsaken, hva må gjøres
- Deretter handlingsplan, deretter data og analyse som underbygger konklusjonen
- Tabeller med ren tekst, ikke fargekoder eller symboler
- Profesjonelt språk — ingen dramatisering eller markedsføringsspråk

1. **Markdown-rapport** (lagres i claudedocs/):
   ```
   claudedocs/overnight_logs/YYYYMMDD_{anleggsnavn}_diagnostic_report.md
   ```

2. **Rapportstruktur** (Nivåmetoden):
   ```
   # [Anlegg] — Diagnostisk Rapport
   **Dato** | **Plant ID** | **Kapasitet** | **Idriftsettelse**

   ## HOVEDBUDSKAP (~100 ord)
   Hva er galt, hva er årsaken, hva må gjøres. Rett på sak.

   ## HANDLINGSPLAN
   KREVER HANDLING: (nummerert liste)
   INGEN HANDLING: (forklaring på hvorfor)

   ## INVERTERSTATUS (tabell)
   ## [PROBLEMKATEGORI 1] (data + analyse)
   ## [PROBLEMKATEGORI 2] (data + analyse)
   ## MPPT-DETALJER (per inverter)
   ## PRODUKSJON (månedlig + ytelsesberegning)
   ## TIDSLINJE
   ## APPENDIKS (alarmer, nettparametre, datakilder)
   ```

3. **Anbefalinger** i handlingsplanen:
   - KREVER HANDLING: Nummerert liste med konkrete steg
   - INGEN HANDLING: Kort forklaring (f.eks. "snørelatert, normaliseres om våren")
   - Ikke overdriv alvorligheten — vinterproduksjonstap er normalt i Norge

---

## Referanser

### Growatt API endpoints brukt
| Endpoint | Bruk | Rate limit |
|----------|------|-----------|
| `/plant/list` | Finn alle anlegg | 5s delay |
| `/device/list` | Inverterliste | 5s delay |
| `/device/inverter/last_new_data` | Sanntidsdata | 5s delay |
| `/device/inverter/data` | Historisk (start_date/end_date) | 5s delay |
| `/device/inverter/alarm` | Alarmer (date param påkrevd) | 5s delay |
| `/plant/power` | Dagskurve (plant-nivå) | 5s delay |

### Dokumentasjon
- IEA PVPS T13-19: PV Failure Monitoring
- IEA PVPS T13-22: Performance Loss Rate Assessment
- Anbefalte Indikatorer for Overvåking av Solcelleanlegg (intern)
- Growatt Server API Guide (research/driftsovervåking/)

### Kjente Growatt-quirks
- **Alle plants returnerer verdier i Watts** — bruk `max_val > capacity_kwp * 2` for deteksjon
- **Rate limiting**: error_code 10012 ved for hyppige kall, bruk **8s delay** (5s minimum), **15s** etter rate limit
- **perpage maks 100**: error_code 10013 "The number of pages cannot exceed 100" ved perpage>100
- **Content-type**: Growatt returnerer `text/html;charset=UTF-8` selv for JSON-svar — sjekk IKKE content-type, bruk try/except på `.json()`
- **SN-mapping**: Noen invertere har ulike SN for last_new_data vs alarm/data endpoints
- **IT-nett**: vacr ≈ 130-138V er normalt (230V/√3)
- **Datoformat**: alarm-endpoint krever `date` param, data-endpoint bruker `start_date`/`end_date`
- **Historisk data**: Returnerer 5-min intervaller, filtrer for pac>0 for å finne dagslys
- **Paginering**: API returnerer kronologisk, page=1 gir ettermiddag/kveld — trenger page 2-3 for morgendata
- **Telleranomalitet**: powerTotal/epvTotal ratio kan være >1.0 (fysisk umulig) — kjent firmware-bug

### Eksisterende scripts
- `scripts/list_all_plants.py` — List alle anlegg med kapasitet
- `scripts/helvik_analysis.py` — Helvik-spesifikk analyse (mal for nye)
- `scripts/morgensjekk_runner.py` — Daglig morgensjekk

---

## Eksempel: Funn fra Finsnes-analysen (22. feb 2026)

Den mest grundige analysen hittil, brukt som referanse:

| Problem | Metode | Funn |
|---------|--------|------|
| Halv DC-spenning | MPPT sammenligning over 7 datoer | INV4 MPPT1/2 = 40% av normal |
| Offline inverter | Telemetri-gjennomgang | DC tilstede men pac=0 = standby |
| Ukjent alarm | Frekvensanalyse + distribusjon | Kode 908 = firmware-spesifikk |
| Stram frekvensgrense | Konfigurasjonslesning | 50.1 Hz → bør være 51.5 Hz |

**Rapport**: `claudedocs/overnight_logs/20260222_finsnes_diagnostic_report.md`

## Eksempel: Funn fra Helvik-analysen (22. feb 2026)

| Problem | Metode | Funn |
|---------|--------|------|
| Død MPPT | Lifetime energibalanse | INV1 MPPT1 = 8.3 kWh vs 20,000+ gjennomsnitt |
| MPPT-gruppering | Ratio analyse | Høy-gruppe (2 strenger): ~50k kWh, Medium (1 streng): ~20k kWh |
| Spenningsfall | Historisk spenning over 3 datoer | MPPT10 vpv synkende: 360→181→125V |
| Telleranomalitet | AC/DC ratio | INV2: powerTotal > epvTotal (ratio 1.12, fysisk umulig) |

**API-lærdommer**:
- `perpage` maks 100 (ikke 200)
- Content-type alltid `text/html` uansett — ikke sjekk den
- Page 1 gir siste 100 records (ettermiddag) — trenger paginering for morgen

**Rapport**: `claudedocs/overnight_logs/20260222_helvik_diagnostic_report.md`

---

## Workflow som Claude Code skill

Når denne skillen invokeres:

1. **Parse input** — finn anleggsnavn/plant_id
2. **Kjør Fase 1-2** i parallell der mulig (flere Read-kall)
3. **Kjør Fase 3-4** sekvensielt (API rate limiting)
4. **Kjør Fase 5** med data fra fase 1-4
5. **Kjør Fase 6** — hypotesetesting (iterativt til over 80% konfidens)
6. **Generer rapport** (Fase 7) — Nivåmetoden, rett på hovedbudskap
7. **Oppsummer** med prioritert handlingsplan

**Forventet tid**: 15-30 min (avhengig av antall invertere og rate limiting)

## Eksempel: Funn fra Solheimen-analysen (22. feb 2026)

Mest komplett analyse med full hypotesetesting:

| Problem | Hypoteser testet | Konklusjon | Konfidens |
|---------|-----------------|------------|-----------|
| Intermitterende MPPTs | 4 (snø, løse koblinger, combiner, firmware) | SNØ | over 90% |
| INV4+INV5 stoppet | 3 (jordfeil, nettfeil, DC-bryter) | Jordfeil (isolasjon 0 kOhm) | Høy |
| INV5 MPPT4 død | 1 (frakoblet/brent sikring) | Aldri tilkoblet | Høy |

Snøhypotesen ble bekreftet gjennom:
- 10 datapunkter med temperaturkorrelasjon (over 0 C = alle MPPTs, under -6 C = kun MPPT4)
- Snøklassifisering fra V/I-signaturer (bypass-diodemodus)
- Falsifisering av H4 (firmware) via klar himmel + høy GHI uten produksjon

**Rapport**: `claudedocs/overnight_logs/20260222_solheimen_diagnostic_report.md`
