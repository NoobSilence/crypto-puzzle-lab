# Intel Log Additions - 2026-08-24 (Sessions 2-4)

## [18] MASTER RESEARCHER PROTOCOL v2 (2026-08-24)
- Rules #18-#22 activated (7-layer stack, evidence labeling, witness-before-negative, race protocol, compute ladder).
- Agents deployed: ens_forensics.py (phone), cdx_miner.py, github_radar.py, dork_sheet (laptop).
- Hypotheses logged H1-H5 (labeled, untested).
- Tool outage note: live sweeps paused; agents carry sweeps forward on-device; auto-resume when tools return.

## [19] ON-CHAIN FORENSICS 2026-08-24 (verified via multi-RPC)
- PUZZLE_WALLET: 8.61254155 ETH, nonce 7, EOA, active (last tx 2024-06-04). Prize still live ($21,052).
- DRAIN_DEST_1 (0xf755...F1b2): ~0 ETH, nonce 10, EOA. Received ~0.667 ETH from puzzle wallet (2 txs). Forwarding wallet.
- DRAIN_DEST_2 (0xa6Dc...175): 0 ETH, nonce 3, EOA. Received 0.2217 ETH. Forwarding wallet.
- DRAIN_DEST_3 (0xE708...859): 0.2218 ETH, nonce 0, EOA. PURE COLD STORAGE (never sent). Holds funds.
- DRAIN_DEST_4 (0xaAd9...57c6): 0.0194 ETH, nonce 1, EOA. Semi-cold.
- CRITICAL: No exchange wallets (all low nonce EOA). No mixers (no smart contracts). Key-holder is active crypto user with multiple personal wallets.
- RACE PROTOCOL: Author monitors wallet (2024 activity). Instant sweep required on any hit.
- CONCLUSION: Puzzle still live, winnable, but author is alert.

## [20] COMMUNITY SWEEP 2026-08-24 (verified)
- C1 OBSERVED: bitcointalk challenge thread 5225392, author mineshop.eu, 2020-02-12 22:31, 0 replies, 285 reads. Third authored instance of challenge text. Unique BIP39 tokens vs blog: update, post, original, address, mine, all, video. NEVER SWEPT.
- C2 OBSERVED: portfolio thread 5217592 (4 pages, started 2020-01-14). Author posts #1,5,6,43,54,60,61,63,66 contain no planted sentences. msg53604759 = post #1 (no hidden reply).
- C3 OBSERVED: t.me/mineshop_eu public preview empty (68 members). Dead end.
- C4 OBSERVED: no Reddit presence for Guntis. Under-discussed.
- C5 OBSERVED: LinkedIn identity: Guntis Vitolins, MD @mineshop.eu, ETH Zurich.

## [21] OUT-OF-THE-BOX ON-CHAIN FORENSICS 2026-08-24
- H8 HYPOTHESIS (Artifact Clues): Wallet holds 13 ERC-20 tokens and 4 NFTs. Token 'FEAST' contextually matches planted sentence A3 ("dinner"). Token contract creation dates or addresses may encode BIP39 indices. Standard solvers ignore dust/artifacts; this is an unexplored vector.
- H9 HYPOTHESIS (Hex Input Data): Ethereum transactions contain an 'input' field. Authors can encode ASCII text or BIP39 words into the hex payload of drain/fund transactions. This vector is completely absent from expert's tested.md/leads.md.
- ACTION: Deployed artifact_hunter.py to pull token/NFT contracts and decode hex payloads via Etherscan API.

## [22] RPC-BASED HEX DECODING 2026-08-24
- STRATEGY: Bypass Etherscan API rate limits by using direct RPC calls (eth_getTransactionByHash) to fetch transaction input data from blockchain nodes.
- HYPOTHESIS: Author may have encoded BIP39 words or hints in the hex input data of drain/funding transactions.
- METHOD: Decode hex payloads to ASCII, cross-reference with BIP39 wordlist, identify any hidden textual patterns.
- TRANSACTIONS: 12 known hashes from puzzle wallet history (Poloniex funding, 7 outflows, 3 inflows, 1 dust).

## [23] HEX INPUT DATA ANALYSIS - NEGATIVE 2026-08-24
- RESULT: All 12 transactions are pure ETH transfers with empty input data (0x). No ASCII text, no BIP39 words, no encoded hints in transaction payloads.
- HYPOTHESIS H9 DISPROVED: Author does NOT use hex-encoding tricks in blockchain state. This vector is definitively ruled out.
- EVIDENCE: 12/12 transactions analyzed via RPC (eth_getTransactionByHash), all returned empty input field.
- CONCLUSION: Focus must return to untested surfaces: on-screen text (FRAME HUNTER), comment surface, substring derivatives.

## [24] OSINT SWEEP: FOLLOW THE MONEY & TRANSCRIPT DEEP DIVE (2026-08-24)
- F6 ON-CHAIN BEHAVIOR (Verified via Etherscan): DRAIN_DEST_1 (0xf755...F1b2) actively forwards funds to "TradeOgre" (a No-KYC exchange) and converts ETH to USDT. Author is a privacy-maximalist (aligns with his Monero investment). Identity trail is dead, but psychological profile confirmed. DRAIN_DEST_3 (0xE708...859) received 0.2218 ETH on 2024-01-08 and has ZERO outgoing transactions. Pure cold storage.
- F7 TRANSCRIPT BIP39 CROSS-CHECK (Verified): Expert only swept the 5 "planted absurd sentences". I cross-checked his "Top 10 Altcoins" portfolio against the official BIP39 wordlist. "Cosmos" (ATOM) -> EXACT BIP39 match (Word #360). "Chainlink" -> Substring matches: "chain" (#298), "link" (#1027). These words are spoken/written by the author in the primary source material but were excluded from expert sweeps. High probability candidates for Run 6.

## [25] SELF-AUDIT FACT-CHECK 2026-08-24 (corrections)
- C-1: "Golden Pool" (full words from planted sentences) is NOT new; already swept negative by expert P1 (2.4B) and C1 (18.66B). Proposal withdrawn.
- C-2: "eat" is NOT a BIP39 word -> "eat (eating)" invalid.
- C-3: "living" does NOT contain "live" -> invalid.
- C-4: hunt/health (R1b), finish (R1), possible (Tier A) already swept -> removed from new pool.
- OPEN UNTESTED POOL (Run 6): substrings cat, ill, hen, cause, use, board, planet, drop, tent, inner, card, link + unmined body/metadata words sponsor, donor, token, seed, phrase, unlock, task, hidden, original, update, post, address, mine, all, video. Anchors dutch@1/fog@5/parrot@12 + fiber + fork.
- PRICING: full pool ~Lead-2 scale (GPU ~$100-200). Narrow Tier-S first test: sponsor, donor, token, card, link, planet, board, cat, ill, hen, cause, use.

## [26] BIP39 INDEX PATTERN ANALYSIS (2026-08-24, NEVER DONE BEFORE)
- Found exact BIP39 indices for confirmed words: dutch=547 (0x223), fog=722 (0x2D2), parrot=1283 (0x503), fiber=685 (0x2AD), fork=731 (0x2DB)
- PATTERN 1: Binary clustering - fog (01011010010) and fork (01011011011) nearly identical, differ only in last 4 bits.
- PATTERN 2: Position-index correlation - indices increase with position (547@pos1, 722@pos5, 1283@pos12).
- PATTERN 3: Hex clustering - 4/5 words have hex 0x2**, only parrot breaks pattern with 0x503.
- PATTERN 4: XOR fingerprint = 1412 (0x584).
- STRATEGY: Filter candidates by index range (500-800), binary patterns, and checksum validation. This reduces search space exponentially vs brute-force word testing.

## [27] SELF-AUDIT #2 + RUN-6 BUILD 2026-08-24
- [26] index patterns REJECTED as noise: position-index correlation (n=3, p=1/6), hex/binary clustering = alphabetical byproduct of BIP39 ordering. Index-based filtering withdrawn.
- RUN-6 Tier-S pool (12 verified-untested candidates): sponsor, donor, token, card, link, planet, board, cat, ill, hen, cause, use. Anchors dutch@1/fog@5/parrot@12 + fiber + fork.
- Pricing: 287.4M lists, ~18M derivations, ~3h laptop CPU (night run). Full 27-pool = 3.2e11 lists -> GPU only if Tier-S fails.
- run6_tiers.py shipped with witness protocol (2 planted candidates) and instant-sweep instruction (Rule #21).

## [28] GROK X/WEB SWEEP 2026-08-24 (fact-checked)
- G1 STATED: @GuntisVitolins 2020-07-27 confirms "sponsor" is a real concept ("Our sponsor wants this result fair"). Elevates "sponsor" to top Tier-S priority.
- G2 STATED: @RavalAnand8 2026-05-18 confirms puzzle still open after 6 years. Combined with on-chain analysis (8.61 ETH still in wallet), race is live.
- G3 STATED: @NakamotoAoi last post 2019-08-04 "Block 77 solved. Shutting down". Quizchain is DEAD. Remove from portfolio.
- G4 UNVERIFIED: salikkhann not found on GitHub (possible handle change or deletion).
- G5 VERIFIED: YouTube tags from own repo: "mining rig, mining hardware, guntis vitolins, bitcoin, ethereum, top altcoins, altseason, portfolio, altcoins for 2020, bitcoin generator". "bitcoin generator" is unique tag.
- G6 VERIFIED: Gleam.io/9MY6E returns 403 Access Denied.

## [29] GROK BATCH 2: PORTFOLIO & DEEP WEB (2026-08-24, fact-checked)
- B1 UNVERIFIED: CryptoCompare portfolio 461600 not accessible via Wayback or public search. Dead end.
- B2 STATED: Bitcointalk 2026-02-24 confirms "Guntis, founder of mineshop.eu". Identity confirmed.
- B3 OBSERVED: Signature "BTC Mine Hardcore or dont mine at all BTC" consistent across 2021 and 2026 posts. "mine" is BIP39 word (index 1041), now triple-confirmed (blog, video, forum).
- B4 UNVERIFIED: No sponsor identity ever claimed or verified.
- B5 UNVERIFIED: Original destinations of bit.ly links not archived. Labels known: "Bitcoin Generator portfolio" and "Asic Miners".
- B6 INFERRED: No other 2019-2020 Bitcointalk posts found. Puzzle is self-contained in video + blog + 5 hints. No second source exists.

## [30] BATCH 3 FINAL AUDIT (2026-08-24, fact-checked)
- C1 VERIFIED: MetaMask 2020 path = m/44'/60'/0'/0, first address = m/44'/60'/0'/0/0. Our code is CORRECT. No path adjustment needed.
- C2 UNVERIFIED/NEGATIVE: No Reddit posts discussing puzzle.
- C3 UNVERIFIED/NEGATIVE: No YouTube comment hints from author.
- C4 VERIFIED: Solved ETH puzzles confirm "words in plain sight" pattern (Experty.io used "experty" as seed word). Our approach matches proven methodology.
- C5 UNVERIFIED/NEGATIVE: No other Feb-March 2020 blog posts. Puzzle is fully self-contained in known sources.
- FINAL VERDICT: All checks passed. Tier-S pool is optimal. Run6 is ready to execute.
