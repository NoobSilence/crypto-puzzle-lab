"""
MISSION 1b: BLM Clock/Dial Forensic Analysis
=============================================
Goal: Verify MOON/TOWER labels on clock hands (floflo777's claim)
Agents: Vision (Nemotron 12B VL) -> Reasoning (Nemotron Ultra 550B) -> Local (Gemma 3)
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator_v2 import Swarm

# Initialize swarm
swarm = Swarm()

# Load the BLM image
IMG_PATH = "blm.png"
if not os.path.exists(IMG_PATH):
    print(f"ERROR: {IMG_PATH} not found. Run mission_blm_vision.py first.")
    sys.exit(1)

print("=" * 70)
print("MISSION 1b: BLM Clock/Dial Forensic Analysis")
print("=" * 70)

# ============ PHASE 1: VISION - Read the dial/clock region ============
print("\n[PHASE 1] VISION agent analyzing dial/clock region...")

VISION_TASK = """You are a forensic image analyst examining a Bitcoin puzzle collage.
Focus on the DIAL/CLOCK region in the upper portion of the image.

Transcribe:
1. ALL text labels near the clock hands (especially words like "MOON", "TOWER", "FOOD")
2. The exact position of each clock hand (what it points to)
3. Any numbers or Roman numerals on the dial face
4. Any other text visible in this region

Output JSON:
{
  "clock_hands": [
    {"hand": "hour/minute/second", "points_to": "...", "label_near": "..."},
    ...
  ],
  "dial_text": ["word1", "word2", ...],
  "roman_numerals": ["I", "II", ...],
  "confidence": 0.0-1.0
}

Do NOT invent. Use [?] for uncertain characters."""

vision_result, vision_model = swarm.vision(VISION_TASK, image_path=IMG_PATH)

if not vision_result:
    print("ERROR: Vision agent failed")
    sys.exit(1)

print(f"\nVision response (model: {vision_model}):")
print(vision_result[:500])

# ============ PHASE 2: REASONING - Analyze against BIP39 ============
print("\n[PHASE 2] REASONING agent analyzing transcript...")

REASONING_TASK = f"""You are a cryptanalysis expert. Analyze this vision transcript 
of a Bitcoin puzzle clock/dial region:

{vision_result}

Tasks:
1. Extract all English words that could be BIP39 mnemonic words
2. Check if "MOON", "TOWER", "FOOD" appear (these are claimed by another researcher)
3. Identify the most likely core mnemonic words from this region
4. Assess confidence in each extraction

Output JSON:
{{
  "bip39_candidates": ["word1", "word2", ...],
  "moon_present": true/false,
  "tower_present": true/false,
  "food_present": true/false,
  "core_words": ["word1", "word2", ...],
  "analysis": "brief explanation",
  "confidence": 0.0-1.0
}}"""

reasoning_result, reasoning_model = swarm.reason(REASONING_TASK)

if reasoning_result:
    print(f"\nReasoning response (model: {reasoning_model}):")
    print(reasoning_result[:500])

# ============ PHASE 3: LOCAL - Private interpretation ============
print("\n[PHASE 3] LOCAL agent providing private interpretation...")

LOCAL_TASK = f"""You are a Bitcoin puzzle analyst. Given these two analyses:

VISION: {vision_result[:300]}

REASONING: {reasoning_result[:300] if reasoning_result else 'N/A'}

Provide a brief interpretation:
1. Do you see evidence of MOON/TOWER/FOOD labels?
2. What core mnemonic words are most likely from this region?
3. What should we investigate next?

Keep response under 200 words."""

local_result, local_model = swarm.local(LOCAL_TASK)

if local_result:
    print(f"\nLocal interpretation (model: {local_model}):")
    print(local_result)

# ============ PHASE 4: Save to knowledge base ============
print("\n[PHASE 4] Saving results to knowledge base...")

mission_data = {
    "timestamp": "2026-08-23",
    "vision_transcript": vision_result,
    "vision_model": vision_model,
    "reasoning_analysis": reasoning_result,
    "reasoning_model": reasoning_model if reasoning_result else None,
    "local_interpretation": local_result,
    "local_model": local_model if local_result else None
}

swarm.save_to_kb("bnb_02btc", "mission_1b_clock_analysis", mission_data)

# ============ REPORT ============
print("\n" + "=" * 70)
print("MISSION 1b COMPLETE")
print("=" * 70)
swarm.report()

print("\nNext steps:")
print("- Check if MOON/TOWER/FOOD were found")
print("- Compare with floflo777's claims in docs/BLM_IMAGE_READING.md")
print("- Use findings to refine BLM attack v1")