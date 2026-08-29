# Pattern: Supply-Control Rug Pull (RUG-01)

**Pattern ID:** RUG-01
**Severity:** Critical
**Chains Observed:** Solana
**First Documented:** August 29, 2026

## Overview

A supply-control rug pull is a premeditated token launch in which the operator controls the majority of supply through a developer allocation plus a cluster of freshly created wallets, engineers a trust signal (often brand or celebrity impersonation), and dumps into a viral attention window. The dump converts retail attention into exit liquidity within minutes.

This pattern is distinct from opportunistic insider selling: the cluster is funded, activated, and cashed out inside a single operational window, and the funding chain typically leaks KYC data at the entrance while the exit is armored.

## Attack Signature

### Phase 1: Token Deployment
**OBSERVED pattern:**
1. Operator deploys token directly (not via a bonding-curve launchpad)
2. Mint authority retained by the creator wallet
3. No freeze authority, no token extensions
4. Creator wallet funded from a regulated exchange hot wallet

**Detection criteria:**
- Mint address without launchpad suffix (e.g., no "pump" suffix on Solana)
- Creator = mint authority (single address controls both)
- Creator first funded within hours of deployment
- Funding source carries an explorer label (CEX hot wallet)

### Phase 2: Supply Concentration
**OBSERVED pattern:**
1. Developer allocation held openly (e.g., 60% of supply)
2. Cluster of fresh wallets buys additional supply with small amounts
3. Combined control exceeds 80% before any public promotion

**Detection criteria:**
- Dev + cluster control >50% of supply (critical threshold: >80%)
- Cluster wallets created on the same day as the dump
- Identical dust funding amounts to each cluster wallet (±10%)
- Single shared funder wallet for the cluster

### Phase 3: Trust Signal Engineering
**OBSERVED pattern:**
1. Token name/branding mimics an official or celebrity-adjacent brand
2. Impersonator accounts promote the token with links to the official site
3. The official account itself posts nothing about the token

**Detection criteria:**
- Official account handle has zero posts mentioning the token
- Promotion originates from low-follower accounts created recently
- Promotion text links to a legitimate external site (brand laundering)
- Community members publicly ask the brand for authorization (no answer)

**Evidence label:** brand authorization claims are UNVERIFIED until the official account confirms.

### Phase 4: Attention-Window Dump
**OBSERVED pattern:**
1. A viral post (warning or promotion) creates a liquidity window
2. Retail buys into the window, providing exit liquidity
3. Cluster sells the full position within minutes

**Detection criteria:**
- Full cluster sell within <60 minutes of a viral post
- Sell volume equals the cluster's entire buy position
- Return multiple >10x on the cluster's buy cost

### Phase 5: Consolidation and Armored Exit
**OBSERVED pattern:**
1. Sale proceeds consolidate into 1-2 intermediate wallets
2. Funds move to a final unlabeled wallet and sit idle
3. No immediate CEX deposit (operator waits out the heat)

**Detection criteria:**
- Consolidation wallet first activity = same day as dump
- Final destination has no explorer label
- Funds idle >24 hours (waiting behavior)

## KYC Leak Signature

**OBSERVED:** The operator armored the exit but left the entrance wide open - twice:

```text
Regulated On-Ramp #1 (KYC)          Regulated On-Ramp #2 (KYC)
   |                                    |
   +-> Creator wallet                   +-> Cluster funder wallet
        |                                    |
        +-> Token deployment                 +-> 15 fresh cluster wallets
                                                    |
                                                    +-> Dump -> Consolidation -> Unlabeled exit
```

**Why this matters:**
- Both on-ramps maintain KYC records (IP, email, bank/card details)
- Two subpoenas = one identity
- Explorer labels on the funding wallets are third-party attributions; the KYC conclusion is INFERRED until legal process confirms it

## Case Study: $GOLD / Trump Digital Gold (Aug 29, 2026)

**Token:** Trump Digital Gold (GOLD)
**Mint:** EMWtbpHaNqMbjUMZguuazhuZUVLWG3z4C5oZnGJPSqxS

**Timeline (all OBSERVED via Solscan/RPC):**

| Time (UTC) | Event |
|---|---|
| 00:17:00 | Binance-labeled hot wallet (5tzFki...vuAi9) funds cluster wallets |
| 01:21 | Creator wallet (3pQA1Z...fRsr, KuCoin-funded) mints token |
| ~03:30 | Cluster buys 224.5M GOLD for $18,657 |
| 03:35:59 | Lookonchain warning goes viral (210 likes) |
| 03:54:22 | Cluster consolidates sale proceeds to HPj88E...2e6Pa (2,860 SOL) |
| 04:09:49 | 224.5M GOLD dumped for 3,178 SOL ($330K) - 17x return |
| 04:22-04:23 | 2,316 SOL moved to unlabeled wallet H6BHT5...HWEZ |

**Supply control:** dev 600M (60%) + cluster 224.5M (22.45%) = 82.45%

**Impersonation:** @realtrumpcoins1 (followed by @realDonaldTrump) posted zero $GOLD content; impersonator accounts promoted "GET YOUR $GOLD NOW" with links to realtrumpcoins.com. Authorization status UNVERIFIED.

**Launchpad check:** not Pump.fun - no "pump" suffix, Token Extensions False, mint authority retained. (An earlier claim of a Pump.fun launch is DISPROVEN.)

**Full case file:** [cases/gold-rug-2026-08.md](../../cases/gold-rug-2026-08.md)

## Detection Heuristics

### For Investigators
1. Check mint authority and launchpad origin before trusting any brand narrative
2. Sum dev + cluster holdings; >80% control = premeditation, not market dynamics
3. Pull first-transaction timestamps for all large holders; same-day creation = cluster
4. Trace cluster funding backward; a shared CEX-labeled funder = KYC leak
5. Map the dump against viral post timestamps; <60-minute window = attention arbitrage

### For Retail Users
1. Treat celebrity-adjacent token launches as hostile until the official account confirms
2. Check holder concentration on an explorer before buying
3. A viral warning is not a buy signal; attention windows are where insiders exit

### For Protocols/Launchpads
1. Flag tokens whose top wallets share a single funder
2. Alert on same-day wallet creation bursts buying one token
3. Require brand-authorization verification for tokens using official-sounding names

## Indicators of Compromise (IOCs)

### $GOLD Case Addresses
- Token mint: EMWtbpHaNqMbjUMZguuazhuZUVLWG3z4C5oZnGJPSqxS
- Creator: 3pQA1ZCaAuFgVJPmkxUGhBaDQjRpt88CXaXmoVy3fRsr
- Cluster funder (Binance-labeled): 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9
- Consolidation: HPj88EYemrC8ttSAEKzGSd8QThtigcvjosXsYQi2e6Pa
- Intermediate: 4S6gV2KsdNQc3dLLmnwJsJqskMPvkZG8vAs1p5rN6o1W
- Exit (unlabeled, 2,316 SOL): H6BHT5Q9rHnfj8kpUMkUtsDTjeypLDePxm5gkgojHWEZ

### Behavioral Signatures
- Identical dust funding (0.05505 SOL) to multiple wallets in the same minute
- Cluster creation within 4 hours of the dump
- Full-position sell within a 34-minute viral window
- Post-dump consolidation into a single unlabeled wallet

## Tools

### [pattern_detector.py](../../tools/pattern_detector.py)
Detects supply-control signatures by analyzing holder concentration, wallet age, and shared funding sources.

### [cross_chain_tracker.py](../../tools/cross_chain_tracker.py)
Traces consolidation and exit flows to identify the final holding wallet and any later CEX deposit.

**Status:** both tools are early scaffolds; outputs must be manually verified against Solscan/RPC before publication.

## References

- Lookonchain warning: @lookonchain/status/2093543159125115389
- Lookonchain dump report: @lookonchain/status/2093551671272206514
- Authorization question: @BTDC666/status/2093540053171798146
- Our forensic thread: @sprunky_eth/status/2093572579810283531
- Related pattern: [patterns/address-poisoning/dust-drop-activation.md](../address-poisoning/dust-drop-activation.md)

## Changelog

- **2026-08-29:** Initial pattern documentation based on the $GOLD case
- **Status:** signature defined; case file in progress; monitoring exit wallet H6BHT5...HWEZ
