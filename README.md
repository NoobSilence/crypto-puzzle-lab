# Crypto Puzzle Lab
Knowledge base + attack scripts + research methodology for open crypto puzzles.

## Auteur: NoobSilence
Methodoloog voor crypto puzzle research.

---

## Documentatie

| Document | Beschrijving |
|----------|---------------|
| docs/RESEARCH_METHODOLOGY.md | Unieke aanpak en ontdekkingen |
| docs/PUZZLE_INDEX.md | Overzicht van alle puzzels |
| docs/COMMUNITY_RESOURCES.md | Netwerk en collaborators |
| docs/ROADMAP.md | Strategisch plan |
| docs/0.2_BTC_FULL_ANALYSIS.md | BNW/BLM analyse (geparkeerd) |
| docs/10ETH_GUNTIS_FULL_ANALYSIS.md | Guntis analyse (actief) |
| docs/GSMG_PIPELINE.md | GSMG solver |
| docs/TECHNICAL_STACK.md | Laptop setup |

---

## Key Discovery: Tijdlijn-Paradox

0.2 BTC puzzel: De seed bestaat VOOR de image, niet andersom.

- Funding TX: 10 mei 2020
- George Floyd: 25 mei 2020
- Image: Oktober 2020

Implicatie: Image is een private bijection, geen generative recipe.

Dit inzicht wordt gemist door 99% van de solvers.

---

## Actieve Puzzels

### 10 ETH Guntis (Hoogste Prioriteit)
- Adres: 0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF
- Status: 7 checksum-valid combinaties, 0 hit
- Volgende stap: Video frames analyseren

### GSMG
- Adres: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
- Status: Wachtend op Florent's hint

---

## Repository Structuur

```
crypto-puzzle-lab/
├── docs/                     # Alle documentatie
├── knowledge_base/           # JSON per puzzel
└── scripts/                  # Attack + tool scripts
    ├── cert/
    ├── attacks/
    └── tools/
```

---

## Technische Stack

- Python 3.11.3 + embit + coincurve + pycryptodome
- ffmpeg voor video analysis
- yt-dlp voor YouTube downloads
- Git voor version control

Zie: docs/TECHNICAL_STACK.md

---

## Contact

- GitHub: https://github.com/NoobSilence/crypto-puzzle-lab
- Auteur: NoobSilence

---

## License

MIT
