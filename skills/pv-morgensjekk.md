# /pv-morgensjekk - PV Driftsovervåking Morgensjekk

Daglig helsesjekk av alle solcelleanlegg med AI-vurdering av alarmer og avvik.

## Formål

Kjør denne skillen etter soloppgang for å:
1. Sjekke om alle invertere er online
2. Vurdere produksjon vs forventet (justert for tid på dagen)
3. Klassifisere alarmer: KRITISK / UNDERSØK / OK
4. Få AI-forklaring på avvik
5. Sende varsler via Teams/e-post

## Invokasjon

### Automatisk (anbefalt)
Scriptet kjører automatisk kl 11:00 hver dag via cron/systemd.

### Manuelt
```bash
# Full kjøring med varsling
python /mnt/c/users/klaus/klauspython/PVDashboard/scripts/morgensjekk_runner.py --local --verbose

# Test uten varsling
python /mnt/c/users/klaus/klauspython/PVDashboard/scripts/morgensjekk_runner.py --local --dry-run --verbose

# JSON output for debugging
python /mnt/c/users/klaus/klauspython/PVDashboard/scripts/morgensjekk_runner.py --local --json
```

### Fra Claude Code
```bash
/kc:pv-morgensjekk
```

---

## Workflow

### Steg 1: Kjør morgensjekk-runner

```bash
python3 /mnt/c/users/klaus/klauspython/PVDashboard/scripts/morgensjekk_runner.py --local --verbose
```

Scriptet gjør automatisk:
1. Henter data fra alle tenants via API
2. Beregner PR justert for tid på dagen
3. Evaluerer status (regelbasert eller AI)
4. Sender varsler til Teams/e-post

### Steg 2: Les resultat (hvis manuell kjøring)

Basert på dataen, vurder hvert anlegg med følgende kriterier:

#### Klassifisering

**KRITISK** (krever umiddelbar handling):
- Alle invertere offline på et anlegg
- PR = 0 med klarvær og >3 timer siden soloppgang
- Aktive alarmer som ikke har løst seg
- Produksjon <20% av forventet uten værforklaring

**UNDERSØK** (sjekk i løpet av dagen):
- PR 50-70% uten åpenbar forklaring
- Enkeltstående inverter offline
- Ubalanse mellom invertere >15%
- Gjentagende alarm fra tidligere dager

**OK** (ingen handling):
- PR >75% eller forklarbart lavt (overskyet, tidlig morgen)
- Alle invertere online
- Ingen aktive alarmer

### Steg 4: Generer rapport

For hvert anlegg, output:

```
## [TENANT] Anleggsnavn

**Klassifisering**: KRITISK / UNDERSØK / OK
**Konfidensgrad**: X%

**Status**:
- Invertere online: X/Y
- Dagens produksjon: X kWh (forventet: Y kWh)
- Performance Ratio: X%

**Forklaring**:
[AI-generert forklaring på 1-3 setninger]

**Anbefalt handling**:
[Konkret handling hvis ikke OK]
```

### Steg 5: Oppsummering

Avslutt med samlet oversikt:

```
## Oppsummering Morgensjekk [DATO]

| Status | Antall | Anlegg |
|--------|--------|--------|
| KRITISK | X | [liste] |
| UNDERSØK | X | [liste] |
| OK | X | [liste] |

**Neste steg**:
- [ ] Følg opp KRITISKE alarmer umiddelbart
- [ ] Sjekk UNDERSØK-anlegg i løpet av dagen
```

---

## Eksempel output

```
## [KVINESDAL] Omsorgssenter

**Klassifisering**: OK
**Konfidensgrad**: 95%

**Status**:
- Invertere online: 2/2
- Dagens produksjon: 45.2 kWh (forventet: 52 kWh)
- Performance Ratio: 87%

**Forklaring**:
Produksjonen er innenfor normalt nivå. Lett overskyet vær forklarer
litt lavere PR enn optimalt. Begge invertere fungerer som forventet.

---

## [BYRKJEDALSTUNET] Hovedbygg

**Klassifisering**: KRITISK
**Konfidensgrad**: 98%

**Status**:
- Invertere online: 0/2
- Dagens produksjon: 0 kWh (forventet: 38 kWh)
- Performance Ratio: 0%

**Forklaring**:
Begge invertere har vært offline siden 07:45. Det er klarvær og
4 timer siden soloppgang, så dette er ikke værrelatert. Trolig
nettfeil eller inverter-problem.

**Anbefalt handling**:
1. Sjekk om det har vært strømbrudd i området
2. Kontakt installatør for fysisk inspeksjon
3. Varsle kunde om nedetid
```

---

## Tekniske detaljer

### PR-beregning justert for tid på dagen

Scriptet beregner forventet produksjon basert på:
- **Kapasitet (kWp)**: Fra tenant-config eller Growatt API
- **Sesongbaserte soltimer**: 0.8-6.5 timer avhengig av måned
- **Tid på dagen**: Produksjon følger solkurve, ikke lineær
- **Terskler**: Mer leniént om morgenen (<3t), strengere etterpå

### Datakilde
- Cloud: `https://pv-dashboard-xxx.run.app/{tenant}/api/plants`
- Lokal: `http://localhost:8000/{tenant}/api/plants`

### Solposisjon
- Beregnes med `astral` biblioteket
- Fallback til sesongbaserte estimater hvis ikke installert

### Varsling

Konfigureres i `.env` (se `.env.template`):

**Teams webhook**:
```
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/xxxxx
TEAMS_WEBHOOK_CRITICAL=https://outlook.office.com/webhook/yyyyy  # Valgfritt
```

**E-post**:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_TO=drift@norsksolkraft.no
```

### Scheduling

Installer scheduler:
```bash
cd /mnt/c/users/klaus/klauspython/PVDashboard/scripts/scheduling
./setup_scheduler.sh cron      # Cron job (enklest)
./setup_scheduler.sh systemd   # Systemd timer (anbefalt)
./setup_scheduler.sh test      # Test kjøring
```

---

## Filer

| Fil | Beskrivelse |
|-----|-------------|
| `scripts/morgensjekk_runner.py` | Komplett runner med AI + varsling |
| `scripts/morgensjekk_data.py` | Bare datahenting (for manuell analyse) |
| `scripts/scheduling/` | Scheduler-konfigurasjon |
| `scripts/scheduling/.env.template` | Mal for environment-variabler |

---

## Se også

- `/pv-ukesrapport` - Ukentlig ytelsesrapport (planlagt)
- `/pv-månedsvurdering` - Månedlig gjennomgang med degraderingsanalyse (planlagt)
