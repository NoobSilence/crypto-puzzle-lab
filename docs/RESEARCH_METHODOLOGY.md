# Research Methodology

NoobSilence's systematic approach to crypto puzzle research.

## Core Principles

### 1. Certification Protocol
Each stack is first validated against known test vectors:
- embit + coincurve for BTC/ETH derivation
- Keccak-256 for Ethereum addresses
- BIP39 checksum verification

The stack is used on real puzzles only after certification succeeds.

### 2. Fail-Fast Philosophy
- Test small samples first (10-100 candidates)
- Validate assumptions before large runs
- Document what does NOT work as thoroughly as what does

### 3. Evidence-Based Approach
Every claim must be supported by:
- On-chain data (TXID, block height, timestamp)
- Reproducible code
- Cross-certified results

---

## Discovery #1: The Timeline Paradox (0.2 BTC)

### Finding
The BNB/BLM collage (0.2 BTC puzzle) contains a timeline paradox:
- Funding TX: 10 May 2020
- George Floyd died: 25 May 2020 (15 days later)
- Collage created: October 2020

### Implication
The seed existed BEFORE the image. This means:
1. The image may encode the seed through a public check-step
2. The image is not proven to be a private, creator-only mapping
3. Brute force without a documented image-reading hypothesis is inefficient

### Impact on Puzzle Theory
This is a new insight that 99% of solvers miss.
It redefines how we should approach check-step versus generative puzzles.

---

## Discovery #2: Cross-Puzzle Infrastructure

Instead of building a new stack for each puzzle, we are building:
- Generic BIP39/44/84 derivation tools
- Reusable video analysis scripts (ffmpeg + yt-dlp)
- Certified ETH Keccak stack
- Community hint aggregators

This increases our speed exponentially across multiple puzzles.

---

## Research Workflow

1. Identification: Address, value, type, source
2. Data Collection: Gather all hints (video, blog, community)
3. Validation: Checksum + certification
4. Hypothesis Testing: Small samples first
5. Scale or Kill: Scale up if it works, stop if it does not
6. Document: Record everything in the knowledge base

---

## Anti-Patterns (What We Do NOT Do)

- Follow community hints blindly without verification
- Run large brute-force searches before reducing the search space
- Use scripts without certification
- Become emotionally invested in a puzzle
- Chase puzzles that prove unsolvable (fail fast)
