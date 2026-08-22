# Crypto Puzzle Lab

Knowledge base + attack scripts + research methodology for open crypto puzzles.

## Author: NoobSilence
Methodologist for crypto puzzle research.

---

## Documentation

| Document | Description |
|----------|-------------|
| docs/RESEARCH_METHODOLOGY.md | Unique approach and discoveries |
| docs/PUZZLE_INDEX.md | Overview of all puzzles |
| docs/COMMUNITY_RESOURCES.md | Network and collaborators |
| docs/ROADMAP.md | Strategic plan |
| docs/0.2_BTC_FULL_ANALYSIS.md | BNW/BLM analysis (parked) |
| docs/10ETH_GUNTIS_FULL_ANALYSIS.md | Guntis analysis (active) |
| docs/GSMG_PIPELINE.md | GSMG solver |
| docs/TECHNICAL_STACK.md | Laptop setup |

---

## Key Discovery: Timeline Paradox

**0.2 BTC puzzle:** The seed exists BEFORE the image, not the other way around.

- Funding TX: May 10, 2020
- George Floyd: May 25, 2020
- Image: October 2020

**Implication:** Image is a private bijection, not a generative recipe.

This insight is missed by 99% of solvers.

---

## Active Puzzles

### 10 ETH Guntis (Highest Priority)
- Address: 0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF
- Status: 7 checksum-valid combinations, 0 hit
- Next step: Analyze video frames

### GSMG
- Address: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
- Status: Waiting for Florent's hint

---

## Repository Structure

```
crypto-puzzle-lab/
├── docs/                     # All documentation
├── knowledge_base/           # JSON per puzzle
└── scripts/                  # Attack + tool scripts
    ├── cert/
    ├── attacks/
    └── tools/
```

---

## Technical Stack

- Python 3.11.3 + embit + coincurve + pycryptodome
- ffmpeg for video analysis
- yt-dlp for YouTube downloads
- Git for version control

See: docs/TECHNICAL_STACK.md

---

## Contact

- GitHub: https://github.com/NoobSilence/crypto-puzzle-lab
- Author: NoobSilence

---

## License

MIT
