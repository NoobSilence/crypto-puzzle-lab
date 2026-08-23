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
- Rate-limited (temporary): `poolside/laguna-s-2.1:free`, `cohere/north-mini-code:free`, `z-ai/glm-5.2:free`
### M6: Vision hallucination with leading prompts (2026-08-23)
- **What happened:** Mission 1b prompt asked specifically about MOON/TOWER/FOOD labels. Vision agent hallucinated all three with 92% confidence.
- **Reality:** Unbiased prompt showed only 2 clock hands, NO labels, only "1865-202...?" text.
- **Lesson:** Vision agents (especially Nemotron 12B VL) hallucinate when prompts suggest what to look for.
- **Fix:** ALWAYS cross-check vision output with unbiased prompt that doesn't suggest expected content.
- **Rule:** Never trust vision output without independent verification.


