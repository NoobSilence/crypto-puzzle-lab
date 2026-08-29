# Security Research Methodology

This document defines the evidence standards and operational protocols for all security pattern research and on-chain forensics published in this repository.

## Evidence Labeling Protocol

Every claim in security cases and pattern documentation is labeled with one of four statuses:

### OBSERVED
- **Definition:** Direct from blockchain data (Etherscan, Solscan, RPC calls, transaction signatures)
- **Examples:**
  - "Wallet A received 0.05505 SOL from Wallet B at 2026-08-29T00:17:00Z"
  - "Contract X holds 600M tokens (60% of supply)"
  - "Transaction hash 0xabc...xyz shows transfer of 3,178 SOL"
- **Verification:** Anyone can reproduce using public block explorers or RPC endpoints

### INFERRED
- **Definition:** Logically derived from OBSERVED data with high confidence (>90%)
- **Examples:**
  - "15 wallets created at 00:17 UTC, all funded with identical 0.05505 SOL dust -> coordinated cluster"
  - "Exit wallet moved to Binance deposit address -> cash-out attempt"
  - "82.45% supply control before dump -> premeditated rug pull"
- **Requirements:** Must cite the OBSERVED data it derives from

### UNVERIFIED
- **Definition:** Claim that needs additional confirmation
- **Examples:**
  - "Wallet X is labeled 'Binance 2' on Solscan (explorer label, not consensus)"
  - "Final destination of 2,316 SOL may be a mixer (no public label found)"
  - "Operator identity may be linked to KuCoin withdrawal records"
- **Action:** Requires subpoena, KYC data access, or additional on-chain correlation

### DISPROVEN
- **Definition:** Falsified by counter-evidence
- **Examples:**
  - "Token was launched on Pump.fun" -> DISPROVEN (mint address has no "pump" suffix, Token Extensions = False)
  - "Operator used Tornado Cash" -> DISPROVEN (no mixer interactions in funding chain)
- **Action:** Original claim must be removed or clearly marked as incorrect

## Source Attribution

All cases and patterns must cite:
- **Blockchain data:** Explorer URLs, RPC endpoints, transaction hashes
- **External intelligence:** Social media posts (X handles + status IDs), news articles
- **Community research:** Other investigators' findings (with credit and cross-reference)

## Investigation Workflow

### Phase 1: Alert & Triage (0-15 min)
1. Receive alert (Cielo, EtherDrops, X notifications)
2. Verify transaction on public explorer
3. Check wallet history (first transaction, funding source, balance)
4. Label initial findings as OBSERVED

### Phase 2: Chain Analysis (15-60 min)
1. Trace funding chain backward (where did the wallet get funds?)
2. Identify cluster patterns (shared funders, identical amounts, timing windows)
3. Map exit flow (where did funds go after the attack?)
4. Cross-reference with known patterns in `patterns/` directory
5. Label derived findings as INFERRED or UNVERIFIED

### Phase 3: Attribution (1-24 hours)
1. Identify regulated on-ramps (CEX deposits, fiat on-ramps)
2. Check for explorer labels (Arkham, Solscan, Etherscan)
3. Document KYC-leak potential (subpoena targets)
4. Label attribution claims as UNVERIFIED (requires legal process)

### Phase 4: Publication (24+ hours)
1. Write case file in `cases/` directory
2. Extract reusable pattern to `patterns/` directory
3. Update monitoring alerts (Cielo, EtherDrops)
4. Publish thread on X with evidence labels
5. Engage with community (sniper replies, collaboration offers)

## Verification Standards

### Blockchain Data
- **Ethereum/EVM:** Etherscan, Blockscout, or direct RPC calls
- **Solana:** Solscan, Solana Explorer, or direct RPC calls
- **Cross-chain:** Verify bridge transactions on both source and destination chains

### External Intelligence
- **X posts:** Cite handle + status ID (e.g., `@handle/status/123456789`)
- **News articles:** Cite publication + URL + publication date
- **Community research:** Credit the investigator and link to their work

### Explorer Labels
- **Caveat:** Explorer labels (Arkham, Solscan, Etherscan) are third-party attributions, not consensus data
- **Requirement:** Always note when a claim relies on an explorer label vs. raw chain data

## Collaboration Protocol

### Sharing Intelligence
- **Public:** Publish findings in `cases/` and `patterns/` with full evidence labels
- **Semi-private:** Share draft findings with trusted investigators via DM for peer review
- **Law enforcement:** Provide full attribution files (wallet addresses, transaction hashes, funding chains) to cybercrime units when victims report

### Credit & Attribution
- **Community findings:** Always credit the original investigator when building on their work
- **Our contributions:** Cite our X handle (@sprunky_eth) and link to published threads
- **Collaborative investigations:** List all contributors in the case file

## Tool Usage

### Detection Scripts
All tools in `tools/` are early scaffolds:
- `pattern-matcher.py` - Match known signatures against new activity
- `pattern_detector.py` - Identify cluster wallets via funding patterns
- `cross_chain_tracker.py` - Trace multi-chain movements
- `pre-emptive-hunter.py` - Predict next target based on pattern frequency
- `bounty_hunter.py` - Scan for white-hat opportunities

**Status:** Core logic defined, not yet wired to live blockchain data sources.

### Manual Verification
All tool outputs must be manually verified against public explorers before publication.

## Ethical Guidelines

### Do
- Track attacker wallets to protect future victims
- Document patterns to help protocols patch vulnerabilities
- Share KYC-leak findings with law enforcement (via victims)
- Credit other investigators' work
- Label all claims with evidence status

### Don't
- Dox individuals without legal process
- Publish private keys or seed phrases
- Exploit vulnerabilities for personal gain
- Make attribution claims without evidence
- Use tools for malicious purposes

## Version Control

All methodology updates must be committed with clear commit messages.

This document extends the puzzle-research methodology in [docs/RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md), which covers the OSINT stack, witness-before-negative protocol, and evidence labeling for crypto puzzles.
