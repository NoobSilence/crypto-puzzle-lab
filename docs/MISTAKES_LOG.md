# Mistakes Log - AI Self-Correction Record

This document records failed attempts to prevent repetition. Consult before suggesting tools/APIs/models.

## 2026-08-23 Session Mistakes

### M1: google.generativeai (DEPRECATED)
- **What I suggested:** `pip install google-generativeai`
- **Reality:** Deprecated Nov 2025. Replaced by `google-genai`
- **Lesson:** Always verify package status via web search before suggesting

### M2: Wrong model IDs assumed from training
- **What I suggested:**
  - `gemini-2.5-flash` → does not exist
  - `llama-3.2-11b-vision-preview` → decommissioned
  - `meta-llama/llama-4-scout-17b-16e-instruct` → not on Groq
- **Reality:** Models change frequently; never trust training data
- **Lesson:** ALWAYS verify model IDs via official API or documentation in current session

### M3: Overstating free model availability
- **What I claimed:** "50+ free models on OpenRouter"
- **Reality:** Only 22 free models on the user's account
- **Lesson:** Discovery scripts beat assumptions; verify per-account, not global claims

### M4: Not pre-testing before orchestrator build
- **What I did:** Built orchestrator before verifying individual model availability
- **Reality:** Coding models (poolside, cohere) rate-limited at runtime
- **Lesson:** Test individual models BEFORE building multi-agent architecture

### M5: Wrong fallback logic in logging
- **What happened:** When primary coding model failed, fallback was attempted but not logged
- **Lesson:** Exception handling must log EVERY attempt, not just successes

### M6: Vision hallucination with leading prompts (2026-08-23)
- **What happened:** Mission 1b prompt asked specifically about MOON/TOWER/FOOD labels. Vision agent hallucinated all three with 92% confidence.
- **Reality:** Unbiased prompt showed only 2 clock hands, NO labels, only "1865-202...?" text.
- **Lesson:** Vision agents (especially Nemotron 12B VL) hallucinate when prompts suggest what to look for.
- **Fix:** ALWAYS cross-check vision output with unbiased prompt that doesn't suggest expected content.
- **Rule:** Never trust vision output without independent verification.

## Session 2026-08-29 - Security research day

### M-D13: Sniper reply linked to the wrong thread
- **What happened:** Announced a sniper reply with the $870K thread link before the $GOLD thread existed.
- **Fix:** Publish the relevant thread first, verify it, then reply with the real link.

### M-D14: Fabricated puzzle name
- **What happened:** Used "Black Lotus Mystery" for the BLM collage puzzle without checking existing docs.
- **Reality:** The verified name is "BLM Collage (Welcome to the Brave New World)", per `docs/BLM_IMAGE_READING.md`.
- **Fix:** Verify puzzle names against existing docs before using them in new material.

### M-D15: README referenced files that did not exist
- **What happened:** Drafted README sections linking to case/pattern files before those files were created (dead links).
- **Fix:** Mark not-yet-created files as "planned" in prose (no link syntax) and only add a real link once the file exists.

### M-D16: Premature anchor link
- **What happened:** Proposed a README link to `docs/TECHNICAL_REFERENCES.md#price-feed-vulnerabilities` before that section existed.
- **Fix:** The link was correctly withheld until the target section was created; then linked.

### M-D17: Imprecise characterization of a documentation gap
- **What happened:** A gap-analysis draft described `scripts/run6_tiers.py` on GitHub as "single-thread v3.1" without checking the live file.
- **Reality (verified via marker check):** The live file already uses `multiprocessing`, so "single-thread" was wrong. However, all six specific v4 markers checked for (`HIT_MNEMONIC.txt`, `FLUSH_EVERY = 50000`, `EXPECTED_WITNESS`, `min(mp.cpu_count(), 4)`, `def build_tasks`, `def witness_test`) were genuinely absent, so the underlying gap (missing v4 features) was real.
- **Fix:** State documentation gaps precisely (which named features/markers are missing), not with an inaccurate blanket label like "single-thread".

### M-D18: Reconstructed crypto script committed without full derivation verification would have shipped a broken self-test
- **What happened:** A reconstructed `movie_enigma_master_checker.py` was drafted with a hardcoded BIP84 test-vector address. Running its own self-test failed; an independent cross-check with the already-certified `embit` library reproduced a third, different address, confirming a real bug in the custom BIP32/bech32 implementation rather than an environment issue.
- **Fix:** The script was not committed. Any custom from-scratch key-derivation code must pass its own self-test against a trusted, independent implementation before being added to the repository.

### M7: Voting logic counted mentions not agents (2026-08-23)
- **What happened:** mission_vision_voting.py reported "MOON: CONFIRMED (3/3)" but only Gemini mentioned MOON.
- **Root cause:** Code counted keyword mentions per line, not distinct agents making the claim.
- **Reality:** MOON/TOWER = 1/3 (only Gemini). FOOD = 0/3 (hallucination from mission 1b disproven).
- **Lesson:** Voting/consensus logic must count DISTINCT AGENTS, not total mentions.
- **Fix:** fix_voting_logic.py counts per-agent claim sets using set() per agent.

### M8: Asked human for analysis that AI should do (2026-08-23)
- **What happened:** I asked the user to open blm.png and tell me where the clock is.
- **Why wrong:** Image analysis is AI cognitive work, not a human physical action. Violates hybrid division of labor.
- **Lesson:** The AI must self-analyze via scripts/tools. Never delegate analysis to the human.
- **Fix:** Built auto-detection script that finds the clock region without human input.

### M9: Prompt contamination caused hallucination (2026-08-23)
- **What happened:** Mission 2 prompt mentioned "whitepaper", "payee", "transaction". Nemotron hallucinated the text "THEY WERE RECEIVED THE PAYEE NEEDS POOR" on the dial.
- **Reality:** 3-agent voting confirmed 0/3 agents see this quote. Dial actually has mirrored Latin (UBI BENE IBI PATRIA).
- **Lesson:** Vision prompts must NEVER contain examples or hints about expected content. Any mention of specific words biases the model.
- **Fix:** Unbiased prompts only describe region, never content. Always verify with 3-agent voting (rule 9).

## Models to NEVER suggest (as of 2026-08-23)
- `gemini-2.5-flash` (deprecated)
- `gemini-1.5-pro-latest` (deprecated)
- `llama-3.2-11b-vision-preview` (decommissioned on Groq)
- `meta-llama/llama-4-scout-17b-16e-instruct` (not on Groq free tier)

## Packages to NEVER suggest (as of 2026-08-23)
- `google-generativeai` (replaced by `google-genai`)

## Verified working models (2026-08-23 session)
- OpenRouter: `nvidia/nemotron-nano-12b-v2-vl:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3-super-120b-a12b:free`
- Groq: `qwen/qwen3.6-27b` (vision, 1000 RPD)
- Ollama: `gemma3:4b` (local, 4.3B)
- Gemini: `gemini-3.6-flash` (via google.genai SDK)
- Rate-limited (temporary): `poolside/laguna-s-2.1:free`, `cohere/north-mini-code:free`, `z-ai/glm-5.2:free`