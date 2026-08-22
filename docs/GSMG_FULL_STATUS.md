# GSMG Full Status - 22 augustus 2026

## Targets

- Main: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe (1.2563451 BTC, partially spent)
- Second: 17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa (3.7505531 BTC, never spent)
- Totaal: 5.0068982 BTC (~$315K) - #1 big prize wereldwijd

## Pipeline Reproductie (byte-for-byte, pre-19 aug)

[OK] Bifid decode calibrated on BTCSEED (keyed square DBIFHCEG, row-major, J-skipped, interleaved coordinates)
[OK] Exact 256-symbol object (23-letter alphabet ABCDEFGHKLMNPQRSTUVWXYZ, no I/O/J)
[OK] 29 dropped letters: OOIIOOOIIOOIOIIOIOOOOIOIIOIOI
[OK] Even-stream: 285 chars, 4-letter base-4 object {B,C,D,E}
[OK] 15-byte header + 1312-byte Dualite structuur (41x32 = 16x82)

## Geteste Routes (allemaal negatief)

- 335M direct reductions (reproductie floflo777 tested.md rijen 1-5)
- 94 lore kandidaten + esrever reversals -> small blob oracle (0 PKCS7-valid padding)
- 28 Matrix-trivia quotes (Architect/Neo/Morpheus)
- 16x16 grid walks (4 direction mappings x 5 start positions)
- Morse/binary/base-N decodings van dropped letters
- XOR-folds / Base58-mod-n / Base4-mod-n
- Community base10->hex decodes (dbbi, z-blocks)
- 6 extreme OpenSSL variants (sha256/md5 KDF x raw/hashed passwords)
- Dualite blob met alle kandidaten
- 5 visuele/semantische hypotheses (Netpbm, SHA BEFORE, matrix sum list literal, LIRPA, BCDE music nibbles)

## NIEUWE Intel (19-21 aug, floflo777 updates)

1. Oracle key-derivation was FOUT tot 2026-08-19 -> alle AES-negatieven moeten RERUN (lead #1)
2. SalPhaseIon pagina publiceert de small blob; de eigen tekst noemt het password (lead #2)
3. Dualite blob gate waarschijnlijk het TWEEDE adres; nooit een password tegen getest
4. r/bitcoinpuzzles threads toegevoegd als bronnen (PR wayzeek, 21 aug)
5. Replay dynamically-constructed candidates die de filter bug nooit bereikte (lead #3)

## BELANGRIJKE CAVEAT

Onze eerdere conclusie 'computational search space exhaustively proven empty' is ONGELDIG: de tests draaiden tegen de verkeerde oracle-derivation. Re-run vereist.

## Correspondentie Log

- 2026-08-18/19: Telegram aan Florent: volledige reproductie + vraag (tool-naam OF private candidate generator)
- 2026-08-19 01:06: Florent reply: holiday until Friday, checkt zodra terug aan computer
- 2026-08-21: Friday - Florent terug (GitHub commits zichtbaar)
- 2026-08-22: Nog geen reply; plan: maandag update sturen MET re-run resultaten

## Actieplan

1. Re-run alle kandidaat-families door gecorrigeerde oracle (sha256(X) password, OpenSSL Salted__ AES-256-CBC)
2. SalPhaseIon pagina text extracten voor password-kandidaten
3. Dualite blob testen tegen tweede escrow 17ucy...fyHa
4. Resultaten rapporteren aan Florent (Telegram) + hier documenteren
