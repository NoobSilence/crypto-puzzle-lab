# Pattern: Dust-Drop Activation (Address Poisoning)

**Pattern ID:** AP-001
**Severity:** Medium-High
**Chains Observed:** Ethereum, BSC, Base, Arbitrum
**First Documented:** August 2026

## Overview

Address poisoning is a social engineering attack where an attacker sends small "dust" transactions to a victim's wallet, creating fake transaction history entries that mimic legitimate transfers. The victim, when copying a recent address from their transaction history, accidentally copies the attacker's address instead of the intended recipient.

The **dust-drop activation variant** uses minimal gas funding (typically <0.1 ETH) from regulated on-ramps, creating a KYC trail that can be traced back to the operator.

## Attack Signature

### Phase 1: Gas Station Setup
**OBSERVED Pattern:**
1. Attacker creates "gas station" wallet (Wallet A)
2. Wallet A funded via regulated exchange (CEX or fiat on-ramp)
3. Wallet A holds minimal balance (0.01-0.05 ETH equivalent)
4. Wallet A used exclusively for dust transactions

**Detection Criteria:**
- Wallet created within 30 days of first dust transaction
- Funding source: CEX hot wallet (Binance, KuCoin, Coinbase) or fiat on-ramp (Mercuryo, MoonPay, Transak)
- Balance: <0.1 ETH equivalent
- Transaction count: <50 before dust campaign begins

### Phase 2: Dust Campaign
**OBSERVED Pattern:**
1. Attacker generates "poison" addresses similar to victim's frequent contacts
   - Same prefix (first 4-6 characters)
   - Same suffix (last 4-6 characters)
   - Middle characters differ
2. Attacker sends dust transactions (0.000001-0.001 ETH) from gas station to victim
3. Transactions appear in victim's recent history
4. Victim copies address from history -> sends funds to poison address

**Detection Criteria:**
- Multiple wallets sending identical dust amounts (±10%)
- Transactions clustered in <1 hour window
- Dust amounts: 0.000001-0.001 ETH (too small for legitimate transfers)
- No return transactions (attacker doesn't send back)

### Phase 3: Exit
**OBSERVED Pattern:**
1. Victim sends funds to poison address
2. Attacker immediately forwards to consolidation wallet
3. Consolidation wallet uses privacy tools (bridges, mixers) or splits across multiple chains
4. Final destination: unlabeled wallet or CEX deposit

**Detection Criteria:**
- Poison address balance: 0 (funds moved within 1 hour)
- Consolidation wallet receives from multiple poison addresses
- Exit uses: Tornado Cash, privacy bridges, no-KYC exchanges

## KYC Leak Signature

**OBSERVED:** The gas station wallet funding creates a forensic trail.

**Why This Matters:**
- Regulated on-ramps maintain KYC records (IP, email, bank/card details)
- One subpoena = operator identity
- Attacker protects exit (privacy tools) but leaves entrance wide open

**Evidence Label:** INFERRED (subpoena required for confirmation)

## Case Studies

### Case 1: $870K Wallet Drain (August 2026)

**Incident:** Victim's wallet drained of $870K via address poisoning.

**Findings:**
- Two KYC leaks: Bitfinex (Dec 2024) + Mercuryo (Jun 2025)
- Wallet reuse across 607 days (poor OPSEC)
- Exit armored (privacy bridges, no-KYC exchanges)
- Entrance wide open (regulated on-ramps)

**Evidence Labels:**
- Funding chain: OBSERVED (Etherscan)
- KYC leak potential: INFERRED (subpoena required)
- Operator identity: UNVERIFIED (requires legal process)

**Full Case:** [cases/address-poisoning-2026.md](../../cases/address-poisoning-2026.md)

## Detection Heuristics

### For Victims (Prevention)
1. **Always verify full address** - don't rely on recent transaction history
2. **Use address book** - save frequent contacts with labels
3. **Check transaction amounts** - dust transactions (<0.001 ETH) are red flags
4. **Verify on multiple explorers** - Etherscan + Blockscout + direct RPC

### For Investigators (Post-Attack)
1. **Trace gas station funding** - where did Wallet A get funds?
2. **Check for regulated on-ramps** - CEX deposits, fiat on-ramps
3. **Document KYC leak potential** - which exchanges have logs?
4. **Monitor exit flow** - where did victim's funds go?
5. **Cross-reference with known patterns** - is this a repeat operator?

### For Protocols (Prevention)
1. **Warn users about dust transactions** - UI alerts for <0.001 ETH transfers
2. **Implement address similarity detection** - flag addresses with matching prefix/suffix
3. **Require manual confirmation** - for transactions to new addresses
4. **Educate users** - blog posts, in-app tutorials about address poisoning

## Tools

### [pattern_detector.py](../../tools/pattern_detector.py)
Detects dust-drop activation patterns by analyzing:
- Identical dust amounts (±10%)
- Shared gas station wallets
- Regulated on-ramp funding
- Timing clusters (<1 hour windows)

**Usage:**
```bash
python tools/pattern_detector.py --chain ethereum --target-wallet 0x...
```

Expected output:
```json
{
  "pattern_detected": "dust-drop-activation",
  "confidence": 0.94,
  "gas_station": "0x0b47...0dda",
  "funding_source": "Bitfinex Hot Wallet",
  "kyc_leak": true,
  "poison_addresses": ["0x599B...a71d", "0x8A3C...f4e2"],
  "victim_loss": "$870,000"
}
```
