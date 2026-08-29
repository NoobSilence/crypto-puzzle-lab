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

## Price Feed Vulnerabilities

**Added:** August 29, 2026
**Related pattern:** [patterns/oracle-manipulation/spot-price-vulnerability.md](../patterns/oracle-manipulation/spot-price-vulnerability.md)
**Related case:** [cases/moonwell-2026-08.md](../cases/moonwell-2026-08.md)

### Vulnerability class

Protocols that read instantaneous (spot) prices from on-chain liquidity pools inherit the manipulability of those pools. A spot price is a function of the pool's current reserves; any actor who can temporarily move the reserves can move the price the protocol trusts.

**Established mechanics (background knowledge):**
1. Attacker takes a flash loan of the target asset
2. Attacker swaps against the pool the protocol reads, skewing reserves
3. Protocol computes a distorted price (collateral value inflated, or asset value deflated)
4. Attacker extracts value (borrow against inflated collateral, liquidate at distorted prices, mint at stale rates)
5. Attacker repays the flash loan in the same atomic transaction

**Why flash loans matter:** they remove the capital requirement, making manipulation executable by anyone within a single transaction.

### Signature we track

From our analysis of the Moonwell $8.7M exploit (Aug 27, 2026) and two prior Base incidents:
- Single-transaction drain preceded by a large same-transaction pool skew
- Protocol reads a spot price from a low-liquidity pool
- No TWAP window, no external oracle fallback, no circuit breaker
- Same attack vector reused across different victims

**Evidence label:** per-incident mechanics are OBSERVED in the case files; the cross-protocol signature is OBSERVED via comparative analysis; next-target predictions derived from it are INFERRED and require manual verification.

### Detection checklist (for investigators)

1. Identify which price source the protocol reads (pool address, oracle feed)
2. Compare pool liquidity depth against position size (shallow pool + large read = risk)
3. Check for TWAP usage and window length (short windows remain manipulable)
4. Look for a large same-transaction swap immediately before the drain
5. Compare findings against known signatures in `patterns/oracle-manipulation/`

### Mitigations (for protocols)

1. Replace spot reads with TWAP (window of 30+ minutes for high-value markets)
2. Add an external oracle fallback (e.g., Chainlink) with deviation checks
3. Circuit breakers: pause on price deviation beyond a threshold within N blocks
4. Liquidity requirements: only read from pools above a depth threshold
5. Time-locks on large position changes tied to price-dependent actions

### Historical references (background)

- Uniswap V2/V3 TWAP design notes (official documentation)
- Harvest Finance ($33.8M, Oct 2020): spot-price manipulation via strategy interaction
- Mango Markets ($112M, Oct 2022): oracle price manipulation on a thin market

### Active monitoring

- Pattern signature tracked via `tools/pattern-matcher.py` (early scaffold)
- Next-target prediction via `tools/pre-emptive-hunter.py` (early scaffold; INFERRED outputs require manual verification before publication)
