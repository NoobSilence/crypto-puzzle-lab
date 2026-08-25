# GSMG Puzzle - Pipeline

## Target
- Address: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
- Status: Awaiting Florent

## Pipeline

### Step 1: Bifid Cipher
- Key: BTCSEED
- Keyed Square Prefix: DBIFHCEG
- Alfabet: 25 letters (J weg)

### Step 2: 23-Letter Alphabet
- Letters: A-Z without J and Q
- Object: 256 symbols

### Step 3: Final Stage
Decoded text -> private key via:
1. SHA-256(text)
2. SHA-256(SHA-256(text))
3. Hex decode (als tekst hex is)
4. PBKDF2 met GSMG salt
5. Raw bytes (als tekst 32 bytes is)

## Solver Script
No GSMG solver script is currently included in this repository. The final-stage
methods below document the intended pipeline and should be implemented before
any execution is described as reproducible.

## Status
- Bifid decoding: Working
- Keyed square: Reproduced
- Final stage methods: 5 methods implemented
- Awaiting: Florent's hint
