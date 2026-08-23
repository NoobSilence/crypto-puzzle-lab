"""
MISSION 2: Independent Word Inventory
=====================================
Goal: Read BLM image directly, WITHOUT retracted anchors.
Systematically examine the 3 visible regions floflo777 identified:
  1. Rotated dial with 2 labelled pointers
  2. Pedestal engraving
  3. Right-edge column of ~85 geometric glyphs (3 regions)

This is the highest-value untried work per floflo777.
"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

from orchestrator_v2 import Swarm

swarm = Swarm()
IMG_PATH = "blm.png"

if not os.path.exists(IMG_PATH):
    print(f"ERROR: {IMG_PATH} not found")
    sys.exit(1)

print("=" * 70)
print("MISSION 2: INDEPENDENT WORD INVENTORY")
print("=" * 70)
print("Reading image WITHOUT presupposing anchors")
print()

with open(IMG_PATH, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

# ============================================================================
# REGION 1: PEDESTAL ENGRAVING (below statue)
# ============================================================================
REGION1_PROMPT = """Look at the pedestal/base area BELOW the Statue of Liberty figure.
There is an engraving there.

1. Transcribe EXACTLY every character you can read, in order.
2. Note any uncertain characters as [?].
3. Is there ANY other text near the pedestal (above, below, around)?

Do NOT interpret. Do NOT guess. Output only what is visibly engraved."""

# ============================================================================
# REGION 2: ROTATED DIAL WITH 2 POINTERS
# ============================================================================
REGION2_PROMPT = """Look at the rotated clock/dial face in the image.
There are pointers/hands on it.

1. How many pointers/hands are there?
2. For EACH pointer, describe:
   - What number/position it points to
   - Any text label WRITTEN ON the pointer itself (not near it, ON it)
3. What numbers are visible around the dial?
4. Any text written ON the dial face itself?

Quote text EXACTLY as shown. Do not guess."""

# ============================================================================
# REGION 3: RIGHT-EDGE GLYPHS (~85 total, 3 regions)
# ============================================================================
REGION3_PROMPT = """Look at the right edge of the image. There is a vertical column
of geometric/alphanumeric glyphs. They appear grouped in about 3 regions.

1. Count the total number of distinct glyphs.
2. For EACH glyph (or representative sample if too many), describe:
   - Its shape (circle, triangle, letter-like, symbol)
   - Any recognizable letters or numbers within it
3. How are the 3 regions separated/structured?
4. Does this look like a substitution cipher, a list, or something else?

Do not invent glyphs. If a glyph is unclear, say "unclear [position N]"."""

# ============================================================================
# GENERAL SCAN: anything else visible
# ============================================================================
GENERAL_PROMPT = """Scan the ENTIRE image for any readable text we might have missed.

List EVERY distinct word or phrase you can read, with its approximate location:
- Top area
- Middle area
- Bottom area
- Left edge
- Right edge

Include:
- BLM protest slogans
- Names (historical figures, activists)
- Dates
- Any other text

Format: "LOCATION: text" for each item."""

# Run all regions with the VISION agent
print("[Region 1] Pedestal engraving...")
region1, _ = swarm.vision(REGION1_PROMPT, image_path=IMG_PATH)
if region1: print(f"  OK ({len(region1)} chars)")

print("[Region 2] Rotated dial with pointers...")
region2, _ = swarm.vision(REGION2_PROMPT, image_path=IMG_PATH)
if region2: print(f"  OK ({len(region2)} chars)")

print("[Region 3] Right-edge glyphs...")
region3, _ = swarm.vision(REGION3_PROMPT, image_path=IMG_PATH)
if region3: print(f"  OK ({len(region3)} chars)")

print("[General] Other visible text...")
general, _ = swarm.vision(GENERAL_PROMPT, image_path=IMG_PATH)
if general: print(f"  OK ({len(general)} chars)")

# ============================================================================
# Print all results
# ============================================================================
print("\n" + "=" * 70)
print("REGION 1: PEDESTAL ENGRAVING")
print("=" * 70)
print(region1 or "NO RESPONSE")

print("\n" + "=" * 70)
print("REGION 2: ROTATED DIAL WITH POINTERS")
print("=" * 70)
print(region2 or "NO RESPONSE")

print("\n" + "=" * 70)
print("REGION 3: RIGHT-EDGE GLYPHS")
print("=" * 70)
print(region3 or "NO RESPONSE")

print("\n" + "=" * 70)
print("GENERAL: OTHER VISIBLE TEXT")
print("=" * 70)
print(general or "NO RESPONSE")

# ============================================================================
# Save to KB
# ============================================================================
inventory = {
    "timestamp": "2026-08-23",
    "method": "Independent reading, no retracted anchors",
    "regions": {
        "pedestal": region1,
        "dial_pointers": region2,
        "right_glyphs": region3,
        "general_scan": general
    },
    "context": "Based on floflo777's reply on issue #12 - re-derive word inventory without contaminated anchors"
}

swarm.save_to_kb("bnb_02btc", "mission_2_independent_inventory", inventory)

print("\n" + "=" * 70)
print("MISSION 2 COMPLETE")
print("=" * 70)
print("Next: compare with floflo777's reading, identify overlaps")