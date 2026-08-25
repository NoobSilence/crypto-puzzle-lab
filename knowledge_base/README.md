# Knowledge Base

This directory stores machine-readable research outputs produced by the analysis scripts.

## File Convention

Each JSON file is keyed by puzzle identifier:

- `bnb_02btc.json` - BLM/BNW 0.2 BTC puzzle
- `guntis_10eth.json` - Guntis 10 ETH challenge
- `gsmg.json` - GSMG puzzle
- `corey_1btc.json` - Corey Haines 1 BTC puzzle
- `keysa_100k.json` - Keysa 100K ETH puzzle
- `puzzle_310btc.json` - Bitcoin Puzzle Transaction
- `external_research.json` - External research notes
- `twitter_micro_puzzles.json` - Twitter/X micro-puzzle inventory

Scripts update these files by puzzle ID and analysis key. Keep backups and temporary exports clearly marked with a `.backup` suffix and do not treat them as canonical results.

## Data Policy

- Store evidence and machine-readable results here; keep narrative interpretation in `docs/`.
- Preserve source URLs, timestamps, and evidence labels when recording new findings.
- Never store API keys, seed phrases, private keys, or other secrets in this directory.
