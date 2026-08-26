# Technical References

This page records authoritative standards that constrain mnemonic and derivation research in this repository.

## BIP-39: Mnemonic Codes

Official specification: [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)

Relevant facts for puzzle analysis:

- BIP-39 describes mnemonics for transporting computer-generated entropy into deterministic wallets.
- A 12-word mnemonic represents 128 bits of entropy plus a 4-bit checksum. The general formula is `MS = (ENT + CS) / 11`, with `CS = ENT / 32`.
- Checksum validation confirms structural validity; it does not prove that a candidate is the intended wallet phrase. The specification notes that the checksum is short and random errors can pass validation.
- A phrase assembled from user-created words can be processed, but it is not the normal BIP-39 generation flow. Candidate research should therefore label such phrases as hypotheses rather than generated mnemonics.
- The mnemonic-to-seed conversion uses PBKDF2-HMAC-SHA512 with 2048 iterations. The passphrase is part of the salt, so every different passphrase produces a different valid seed and wallet.
- The English wordlist is the most broadly supported wordlist and should be treated as the default unless primary evidence says otherwise.

## BIP-44: Deterministic Wallet Paths

Official specification: [BIP-44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)

The standard path shape is:

```text
m / purpose' / coin_type' / account' / change / address_index
```

Important implications:

- The apostrophe marks hardened derivation at the purpose, coin type, and account levels.
- External addresses use change index `0`; internal change addresses use `1`.
- Address discovery is convention-dependent. Testing one path is not proof that another wallet implementation did not use a different path, account, change chain, or address index.
- A reproducible sweep should record the exact derivation path, wordlist, passphrase, address type, and implementation used.

## Research Rules Derived from These Standards

1. Treat checksum-valid as a filter, not as confirmation.
2. Test the empty passphrase explicitly and record any additional passphrases separately.
3. Certify derivation code against published test vectors before scanning puzzle candidates.
4. Record all derivation parameters with every result so another researcher can reproduce it.

These notes summarize the official specifications; the standards remain the source of truth.
