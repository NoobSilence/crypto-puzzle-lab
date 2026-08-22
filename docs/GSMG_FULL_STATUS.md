# GSMG Full Status - August 22, 2026

## Targets

- Main: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe (1.2563451 BTC, partially spent)
- Second: 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa (3.7505531 BTC, never spent)
- Total: 5.0068982 BTC (~$315K) - #1 big prize worldwide

## Pipeline Reproduction (byte-for-byte, pre-Aug 19)

[OK] Bifid decode calibrated on BTCSEED (keyed square DBIFHCEG, row-major, J-skipped, interleaved coordinates)
[OK] Exact 256-symbol object (23-letter alphabet ABCDEFGHKLMNPQRSTUVWXYZ, no I/O/J)
[OK] 29 dropped letters: OOIIOOOIIOOIOIIOIOOOOIOIIOIOI
[OK] Even-stream: 285 chars, 4-letter base-4 object {B,C,D,E}
[OK] 15-byte header + 1312-byte Dualite structure (41x32 = 16x82)

## Tested Routes (all negative)

- 335M direct reductions (reproduction of floflo777 tested.md rows 1-5)
- 94 lore candidates + esrever reversals -> small blob oracle (0 PKCS7-valid padding)
- 28 Matrix-trivia quotes (Architect/Neo/Morpheus)
- 16x16 grid walks (4 direction mappings x 5 start positions)
- Morse/binary/base-N decodings of dropped letters
- XOR-folds / Base58-mod-n / Base4-mod-n
- Community base10->hex decodes (dbbi, z-blocks)
- 6 extreme OpenSSL variants (sha256/md5 KDF x raw/hashed passwords)
- Dualite blob with all candidates
- 5 visual/semantic hypotheses (Netpbm, SHA BEFORE, matrix sum list literal, LIRPA, BCDE music nibbles)

## NEW Intel (Aug 19-21, floflo777 updates)

1. Oracle key-derivation was WRONG until 2026-08-19 -> all AES negatives must be RERUN (lead #1)
2. SalPhaseIon page publishes the small blob; its own text names the password (lead #2)
3. Dualite blob likely gates the SECOND address; never had a password tested against it
4. r/bitcoinpuzzles threads added as sources (PR by wayzeek, Aug 21)
5. Replay dynamically-constructed candidates that the filter bug never reached (lead #3)

## IMPORTANT CAVEAT

Our earlier conclusion 'computational search space exhaustively proven empty' is INVALID: tests ran against the wrong oracle-derivation. Re-run required.

## Correspondence Log

- 2026-08-18/19: Telegram to Florent: full reproduction + question (tool name OR private candidate generator)
- 2026-08-19 01:06: Florent replies: holiday until Friday, will check once back at computer
- 2026-08-21: Friday - Florent back (GitHub commits visible)
- 2026-08-22: No reply yet; plan: Monday update WITH re-run results

## Action Plan

1. Re-run all candidate families through corrected oracle (sha256(X) password, OpenSSL Salted__ AES-256-CBC)
2. Extract SalPhaseIon page text for password candidates
3. Test Dualite blob against second escrow 17ucy...fyHa
4. Report results to Florent (Telegram) + document here
