# GSMG Puzzle - Pipeline

## Target
- Adres: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
- Status: Wachtend op Florent

## Pipeline

### Stap 1: Bifid Cipher
- Key: BTCSEED
- Keyed Square Prefix: DBIFHCEG
- Alfabet: 25 letters (J weg)

### Stap 2: 23-Letter Alfabet
- Letters: A-Z zonder J en Q
- Object: 256 symbolen

### Stap 3: Final Stage
Gedecodeerde tekst -> private key via:
1. SHA-256(text)
2. SHA-256(SHA-256(text))
3. Hex decode (als tekst hex is)
4. PBKDF2 met GSMG salt
5. Raw bytes (als tekst 32 bytes is)

## Solver Script
Bestand: scripts/attacks/gsmg/gsmg_final_solver_v2.py

## Status
- Bifid decodering: Werkend
- Keyed square: Gereproduceerd
- Final stage methoden: 5 methoden geimplementeerd
- Wachtend op: Florent's hint
