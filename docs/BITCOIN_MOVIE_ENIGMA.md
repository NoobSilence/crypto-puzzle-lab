# Bitcoin Movie Enigma

**Prize:** 100,000 sats at `bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6`
**Type:** 34 movie stills -> 24-word BIP39 seed (10 intruders dropped via IMDb)
**Status:** Run 1 pending; current list provably unsolvable (see audit)

## Word list (errors marked)

hard, glory, alien, mad, motion, now, escape, goon[X-not-in-BIP39],
sun, possible, ill, life, good, eye, river, warrior,
clock, hope, gravity, first, solar, blade, planet, ordinary,
bar, shark[X-not-in-BIP39], boy, cream, matrix, story, ghost, soft,
shine, human

## Audit findings (2026-08-24)

1. Math claim wrong: ~512K checksum-valid candidates, not ~8.2M (24-word checksum = 8 bits).
2. FATAL: `goon` and `shark` are not BIP39 words; current list cannot contain the solution.

## Fix strategy

- H-BME1: transformation rule = BIP39 word literally in title (Sharknado -> tornado).
- Panel 8 (Goonies) needs re-identification.
- Conflicting panels: 3, 5, 9, 13, 14, 16, 23, 24, 27.
- Find the IMDb criterion that isolates the 10 intruders.

## Tooling

- [scripts/movie_enigma_combo_generator.py](../scripts/movie_enigma_combo_generator.py) - generates checksum-valid 24-word BIP39 subsets from the word list; validated (correctly excludes `goon`/`shark`, ~10.5M combinations, ~41K expected checksum-valid)
- [scripts/make_pdf_report.py](../scripts/make_pdf_report.py) - dependency-free PDF writer for audit reports; validated (produces a well-formed PDF)

**Not yet available:** an on-chain candidate checker. A reconstructed version was built and self-tested against the official BIP84 test vector; the self-test failed and an independent cross-check found its derivation math does not match a trusted reference implementation. It was not committed. A validated checker (for example, one built on `embit`'s certified BIP32/BIP39 derivation instead of a from-scratch implementation) is still needed before any candidate sweep can be trusted.
- [scripts/make_pdf_report.py](../scripts/make_pdf_report.py)
