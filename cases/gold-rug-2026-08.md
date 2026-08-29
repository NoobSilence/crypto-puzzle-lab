# Case: $GOLD (Trump Digital Gold) Rug Pull

**Case ID:** 2026-08-GOLD
**Date:** August 29, 2026
**Chain:** Solana
**Loss:** ~$330K extracted (17x return on $18,657)
**Status:** Active monitoring (exit wallet dormant)
**Pattern:** [patterns/rug-pull/supply-control-signature.md](../patterns/rug-pull/supply-control-signature.md) (RUG-01)

## Executive Summary

On August 29, 2026, a token named Trump Digital Gold ($GOLD) was deployed on Solana, promoted through impersonation of a celebrity-adjacent brand, and fully dumped within hours. The operator controlled 82.45% of supply through a developer allocation and a cluster of freshly created wallets, and sold the entire cluster position into a viral attention window.

Our investigation identified two KYC leaks at the entrance (KuCoin funding the creator wallet; a Binance-labeled hot wallet funding the cluster), while the exit remains armored in an unlabeled wallet holding 2,316 SOL. Two subpoenas to regulated on-ramps would identify the operator.

## Token Facts (OBSERVED)

| Field | Value |
|---|---|
| Name | Trump Digital Gold (GOLD) |
| Mint | EMWtbpHaNqMbjUMZguuazhuZUVLWG3z4C5oZnGJPSqxS |
| Created | 2026-08-29, ~01:21 UTC |
| Creator | 3pQA1ZCaAuFgVJPmkxUGhBaDQjRpt88CXaXmoVy3fRsr |
| Supply | 999,995,086 |
| Holders | 8,761 (as of ~06:45 UTC) |
| Mint authority | Retained by creator |
| Freeze authority | None (Token Extensions False) |
| Launchpad | Not Pump.fun (no "pump" suffix; direct SPL deploy) |

**DISPROVEN claim:** an early hypothesis that $GOLD launched on Pump.fun was falsified by the mint address structure and token configuration.

## Supply Control (OBSERVED)

| Holder Group | Amount | % of Supply |
|---|---|---|
| Developer wallet | 600M | 60.0% |
| 15 cluster wallets | 224.5M | 22.45% |
| **Total control** | **824.5M** | **82.45%** |

Cluster buy cost: $18,657. Cluster sale: 3,178 SOL (~$330K). Profit: ~$312K (17x).

## Timeline (OBSERVED unless noted)

| Time (UTC) | Event |
|---|---|
| 00:17:00 | Binance-labeled hot wallet (5tzFki...vuAi9) funds cluster wallets; four traced wallets show first transaction in the same minute |
| ~01:22 | KuCoin hot wallet funds creator wallet |
| ~01:21-01:26 | Token minted by creator |
| ~03:30 | Cluster completes buys: 224.5M GOLD for $18,657 |
| 03:35:59 | Lookonchain warning goes viral (210 likes, 28 RT) |
| 03:54:22 | Dump executes; proceeds consolidate into HPj88E...2e6Pa (first activity same second) |
| 04:09:49 | Lookonchain publishes dump report |
| 04:21:49 | 57unTW...WHHdV sends 2,936.37 SOL to intermediate 4S6gV2...N6o1W |
| 04:22:51 | 4S6gV2 sends 965.44 SOL to exit wallet H6BHT5...HWEZ |
| 04:23:31 | 4S6gV2 sends 1,350.83 SOL to exit wallet H6BHT5...HWEZ |
| 04:23:35 | HPj88E sends 318 SOL to 4S6gV2 |
| 04:27-04:28 | Dust helper wallet H6BHjm...HWEZ created; sends 0.00001 SOL probes to 4S6gV2 |

**INFERRED:** the dump landed ~18 minutes after the warning went viral; the viral window supplied the buy-side liquidity the cluster sold into. Attention functioned as exit liquidity.

## Funding Chain and KYC Leaks

### Leak 1: KuCoin (creator)
```text
KuCoin Hot Wallet (BmFdpra...WTymy6)
   | ~01:22 UTC
   v
Creator wallet (3pQA1Z...fRsr)
   +-> Minted $GOLD
```

### Leak 2: Binance (cluster)
```text
Binance-labeled hot wallet (5tzFki...vuAi9)
   | 00:17:00 UTC
   v
Cluster wallets (15 total; 4 traced below)
   +-> 9hNRtx...5akz  (sent 407.98 SOL to consolidation)
   +-> 6m58Yw...a6QY  (sent 325.89 SOL)
   +-> CAMHU4...bN4E  (sent 221.67 SOL)
   +-> DFs51y...ga8h  (sent 82.74 SOL)
```

**Label caveat:** "Binance 2" / "Binance Hot Wallet" are explorer labels (Solscan/Arkham), i.e., third-party attributions, not consensus data. The KYC conclusion is INFERRED: regulated exchanges retain withdrawal logs (IP, email, bank/card details); confirmation requires legal process.

**Cluster activation signature:** identical dust drops of 0.05505 SOL from shared activator wallets (3oduNc...ATos, 3odTMN...ATos, 4S6dB8...6o1W) within the same minute windows.

## Exit Flow (OBSERVED)

```text
Cluster sells 224.5M GOLD -> 3,178 SOL
   v
HPj88E...2e6Pa (consolidation; peak 2,860.26 SOL)
   v
4S6gV2...N6o1W (intermediate; peak ~3,255 SOL incl. 2,936 from 57unTW)
   v
H6BHT5...HWEZ (exit; 2,316.27 SOL)
   +-> No explorer label. No further large outflows as of last snapshot.
```

**Assessment:** exit is armored (unlabeled wallet, idle funds = waiting behavior). Entrance was wide open (two regulated on-ramps).

## Impersonation Analysis

- **OBSERVED:** @realtrumpcoins1 (followed by @realDonaldTrump) published zero posts about $GOLD.
- **OBSERVED:** impersonator/affiliate accounts (@thedevrrrrrrr, @ytflzyyds, @Aspirin_2022 and others) promoted "GET YOUR $GOLD NOW: realtrumpcoins.com".
- **OBSERVED:** @BTDC666 publicly asked @realDonaldTrump whether the token was authorized; no authorization observed.
- **OBSERVED:** realtrumpcoins.com is a licensed physical-medallion business (JBCZ Group LLC) whose own terms state products are not manufactured or sold by The Trump Organization.
- **UNVERIFIED:** any affiliation between the token and the realtrumpcoins.com business.

## Open Investigation Items

1. Final destination of the 2,316 SOL if/when H6BHT5...HWEZ moves (CEX deposit = cash-out signal)
2. Creation timestamps for the remaining 11 cluster wallets (4 of 15 traced)
3. Operator identity (requires subpoenas to KuCoin and Binance)

## Actions Taken

- Published forensic thread T1-T6: @sprunky_eth/status/2093572579810283531
- Sniper replies under:
  - @lookonchain/status/2093551671272206514 (dump report)
  - @lookonchain/status/2093543159125115389 (warning)
  - @BTDC666/status/2093540053171798146 (authorization question)
- Monitoring active (Cielo): HPj88E...2e6Pa, 4S6gV2...N6o1W, H6BHT5...HWEZ, 3pQA1Z...fRsr

## Indicators of Compromise (IOCs)

| Type | Address | Role |
|---|---|---|
| Token | EMWtbpHaNqMbjUMZguuazhuZUVLWG3z4C5oZnGJPSqxS | $GOLD mint |
| Wallet | 3pQA1ZCaAuFgVJPmkxUGhBaDQjRpt88CXaXmoVy3fRsr | Creator |
| Wallet | BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6 | KuCoin hot wallet (funder) |
| Wallet | 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9 | Binance-labeled funder (explorer label) |
| Wallet | HPj88EYemrC8ttSAEKzGSd8QThtigcvjosXsYQi2e6Pa | Consolidation |
| Wallet | 4S6gV2KsdNQc3dLLmnwJsJqskMPvkZG8vAs1p5rN6o1W | Intermediate |
| Wallet | H6BHT5Q9rHnfj8kpUMkUtsDTjeypLDePxm5gkgojHWEZ | Exit (2,316 SOL) |
| Wallet | 57unTWh2f3CjdXStDk6Yf7is2C4c7xmb1neZtrCWHHdV | Cluster funding relay |

## Lessons Learned

1. **Attention is a tradable asset.** A viral post - even a warning - creates the liquidity window insiders exit through.
2. **Armored exit, naked entrance.** Operators learn exit OPSEC from public cases but repeatedly leave KYC trails at the funding stage.
3. **Explorer labels are leads, not facts.** Third-party labels guide investigation; legal process confirms it.
4. **Brand laundering works until checked.** Impersonation plus a legitimate external site is a powerful bait; always verify the official account's own posts.

## References

- Lookonchain warning: @lookonchain/status/2093543159125115389
- Lookonchain dump report: @lookonchain/status/2093551671272206514
- Authorization question: @BTDC666/status/2093540053171798146
- Our thread: @sprunky_eth/status/2093572579810283531
- Chain data: Solscan token page, Solscan account pages, Solana mainnet RPC (snapshot 2026-08-29, ~04:30-07:00 UTC)

## Changelog

- **2026-08-29:** Case opened; full timeline and dual KYC leak documented; monitoring active
