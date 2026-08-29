# Case: $870K Address Poisoning Drain (KYC Leak Attribution)

**Case ID:** 2026-08-AP-870K
**Date:** August 10, 2026 (drain); investigation ongoing
**Chain:** EVM (Ethereum mainnet per Etherscan data)
**Loss:** ~$870K (Aug 10 campaign); related Aug 25 campaign ~$500K+
**Status:** Monitoring; exit armored, entrance exposed
**Pattern:** [patterns/address-poisoning/dust-drop-activation.md](../patterns/address-poisoning/dust-drop-activation.md) (AP-001)

## Executive Summary

On August 10, 2026, a victim wallet was drained of ~$870K via address poisoning. The operator's exit was sophisticated (confidential bridges, no-KYC exchanges, multi-chain sharding), but the entrance was left wide open: the gas station wallet was funded by Bitfinex in December 2024, and a sister wallet was topped up via Mercuryo in June 2025.

No Tornado Cash. No mixer. Two regulated on-ramps, two subpoena targets, one operator identity.

This case builds on NoxosIntel's public trace of the drain campaigns; our contribution is the funding-side attribution they did not publish.

## Incident Facts (OBSERVED)

| Field | Value |
|---|---|
| Attack type | Address poisoning (dust-gas activation variant) |
| Drain date | August 10, 2026 |
| Victim loss | ~$870K |
| Attacker wallet | 0x5172...2c0e |
| Related campaign | August 25, 2026 (~$500K+; attacker 0x861EbC...BA55 per NoxosIntel) |
| Mixer usage | None observed |

**Address note:** wallets cited in abbreviated form as published in our thread; full addresses are recoverable from the on-chain record (Etherscan) referenced below.

## Funding Chain (OBSERVED, Etherscan)

```text
BITFINEX Hot Wallet
   | Dec 29, 2024: 0.0141 ETH
   v
WALLET A (0x0b4700d1...0dda) - gas station
   +-> Dec 29, 2024: 0.0139 ETH -> WALLET B (0x599B9491...a71d)
   |       +-> + Jun 20, 2025: 0.026 ETH from MERCURYO (fiat on-ramp)
   |
   +-> Aug 8, 2026: 0.00006 ETH ($0.15) -> ATTACKER WALLET (0x5172...2c0e)
           +-> Aug 10: $870K arrives (victim drain)
           +-> Aug 11-13: swept to dormant wallets
```

Three hops. Two KYC on-ramps. Zero mixers.

## KYC Leaks (INFERRED)

### Leak 1: Bitfinex
- Regulated exchange; KYC required for withdrawals
- Logs retained: IP at funding time, linked email, timestamp correlation

### Leak 2: Mercuryo
- Regulated fiat on-ramp; KYC required
- Logs retained: IP, email, potentially bank/card details

**Conclusion:** one subpoena to Bitfinex plus one to Mercuryo identifies the human behind the cluster. Confirmation requires legal process; identity remains UNVERIFIED.

## OPSEC Asymmetry (OBSERVED)

| Side | Posture | Elements |
|---|---|---|
| Exit | Advanced | Confidential intents (privacy bridges), Baltex (no-KYC instant exchange), multi-chain sharding |
| Entrance | Sloppy | Regulated on-ramps (Bitfinex, Mercuryo), wallet reuse across 607 days, dust gas drops |

**Assessment (INFERRED):** the operator learned exit OPSEC from public cases but ignored entry OPSEC. This is a semi-professional profile: capable enough to execute address poisoning and privacy-bridge exits, careless enough to reuse a Bitfinex-funded wallet across 607 days.

**DISPROVEN hypothesis:** nation-state attribution (e.g., Lazarus Group). State actors use clean genesis wallets and avoid regulated on-ramps entirely; this operator did not.

## Victim Guidance (Actionable)

If you are a victim of the Aug 10 or Aug 25 campaigns:
1. This evidence is actionable for law enforcement
2. Subpoenas to Bitfinex and Mercuryo yield identity
3. Contact your local cybercrime unit and provide the wallet addresses cited above

## Open Investigation Items

1. Full (unabbreviated) wallet addresses for the gas station and sister wallets
2. Linkage between the Aug 10 attacker (0x5172...2c0e) and the Aug 25 attacker (0x861EbC...BA55)
3. Final exit destinations beyond the dormant sweep wallets

## Actions Taken

- Published forensic thread T1-T6: @sprunky_eth/status/2093553961210978570
- Sniper replies under NoxosIntel traces, CryptoKing4Ever, and inno_sol posts
- Peer validation received from NoxosIntel operator (public like + collaboration invite)

## Indicators of Compromise (IOCs)

| Type | Address | Role |
|---|---|---|
| Wallet | 0x0b4700d1...0dda | Gas station (Bitfinex-funded) |
| Wallet | 0x599B9491...a71d | Sister wallet (Mercuryo top-up) |
| Wallet | 0x5172...2c0e | Attacker wallet (Aug 10 drain) |
| Wallet | 0x861EbCC056e0645cF7BA7F5BB528faE9fbA8BA55 | Attacker wallet (Aug 25 campaign, per NoxosIntel) |
| Entity | Bitfinex hot wallet | Funding source (KYC leak 1) |
| Entity | Mercuryo | Fiat on-ramp (KYC leak 2) |

## Lessons Learned

1. **Mixers are not the only trail.** Absence of Tornado Cash does not mean absence of attribution; regulated on-ramps are stronger leads than mixer heuristics.
2. **Wallet reuse is fatal.** A 607-day reuse window turned a single 0.0141 ETH deposit into a full identity path.
3. **Exit OPSEC is learnable; entry OPSEC is neglected.** Public case write-ups teach attackers how to exit; they rarely discipline how attackers fund.
4. **Distributed intelligence works.** NoxosIntel traced the drains; we traced the funding. Together the picture is complete.

## References

- NoxosIntel campaign trace: @NoxosIntel (pinned thread, Aug 2026; Aug 10 and Aug 25 incidents)
- Our funding-chain thread: @sprunky_eth/status/2093553961210978570
- Chain data: Etherscan (OBSERVED)
- Related pattern: [patterns/address-poisoning/dust-drop-activation.md](../patterns/address-poisoning/dust-drop-activation.md)

## Changelog

- **2026-08-29:** Case file created from published thread; evidence labels applied
- **Status:** monitoring dormant sweep wallets; identity attribution pending legal process
