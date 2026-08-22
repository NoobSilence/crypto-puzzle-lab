# Research Methodology

De unieke aanpak van NoobSilence voor crypto puzzle research.

## Kernprincipes

### 1. Certificering-protocol
Elke stack wordt eerst gevalideerd tegen bekende test-vectors:
- embit + coincurve voor BTC/ETH derivatie
- Keccak-256 voor Ethereum adressen
- BIP39 checksum verificatie

Pas als de certificering slaagt, wordt de stack gebruikt voor echte puzzels.

### 2. Fail-Fast Filosofie
- Test kleine samples eerst (10-100 kandidaten)
- Valideer aannames voor grote runs
- Documenteer wat NIET werkt even grondig als wat wel werkt

### 3. Evidence-Based Aanpak
Elke claim moet onderbouwd worden met:
- On-chain data (TXID, block height, timestamp)
- Reproduceerbare code
- Cross-gecertificeerde resultaten

---

## Ontdekking #1: De Tijdlijn-Paradox (0.2 BTC)

### De bevinding
De BNB/BLM collage (0.2 BTC puzzel) bevat een tijdlijn-paradox:
- Funding TX: 10 mei 2020
- George Floyd overleden: 25 mei 2020 (15 dagen later)
- Collage gemaakt: Oktober 2020

### De implicatie
De seed bestond AL voor de image. Dit betekent:
1. De image is een private bijection (check-step)
2. De image is geen generative recipe
3. Brute-force zonder de bijection te kennen is zinloos

### Impact op puzzel-theorie
Dit is een nieuw inzicht dat 99% van de solvers mist.
Het herdefinieert hoe we check-step vs generative puzzels moeten benaderen.

---

## Ontdekking #2: Cross-Puzzle Infrastructuur

In plaats van per puzzel een nieuwe stack, bouwen we:
- Generieke BIP39/44/84 derivation tools
- Herbruikbare video-analyse scripts (ffmpeg + yt-dlp)
- Gecertificeerde ETH Keccak stack
- Community hint aggregators

Dit verhoogt onze snelheid exponentieel over meerdere puzzels.

---

## Research Workflow

1. Identificatie: Adres, waarde, type, bron
2. Data Collection: Alle hints verzamelen (video, blog, community)
3. Validation: Checksum + certificering
4. Hypothesis Testing: Kleine samples eerst
5. Scale or Kill: Opschalen als het werkt, stoppen als het niet werkt
6. Document: Alles vastleggen in de knowledge base

---

## Anti-Patterns (wat we NIET doen)

- Blindelings community hints volgen zonder verificatie
- Grote brute-force runs zonder eerst de ruimte te verkleinen
- Zonder certificering scripts gebruiken
- Emotioneel investeren in een puzzel
- Puzzels najagen die onoplosbaar blijken (fail-fast)
