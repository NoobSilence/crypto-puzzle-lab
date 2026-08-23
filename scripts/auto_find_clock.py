"""
Auto-detect clock region + crop + 3-agent verification
NO human input needed - AI locates the clock itself
"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

from PIL import Image
from orchestrator_v2 import Swarm

swarm = Swarm()
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

IMG_PATH = "blm.png"
img = Image.open(IMG_PATH)
W, H = img.size
print(f"Image dimensions: {W} x {H} pixels")

# Encode full image
with open(IMG_PATH, "rb") as f:
    img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

# Ask vision agent to locate the clock as bounding box fractions
LOCATE_PROMPT = """Look at this Bitcoin puzzle collage. There is a clock/dial somewhere in it.
Tell me where the clock is located as a bounding box using fractions from 0.0 to 1.0.

Output ONLY valid JSON, no other text:
{"left": 0.0-1.0, "top": 0.0-1.0, "right": 0.0-1.0, "bottom": 0.0-1.0}

Where left/top is the top-left corner of the clock and right/bottom is the bottom-right corner."""

print("\n[Step 1] Asking vision agent to locate clock...")
result, model = swarm.vision(LOCATE_PROMPT, image_path=IMG_PATH)
print(f"Raw response from {model}:")
print(result)

# Parse bounding box
try:
    # Extract JSON from response
    start = result.find("{")
    end = result.rfind("}") + 1
    box = json.loads(result[start:end])
    left = max(0, box.get("left", 0.3))
    top = max(0, box.get("top", 0.2))
    right = min(1, box.get("right", 0.7))
    bottom = min(1, box.get("bottom", 0.6))
except Exception as e:
    print(f"Could not parse bounding box ({e}), using default center region")
    left, top, right, bottom = 0.25, 0.15, 0.75, 0.55

# Add padding so we don't cut off the clock
pad = 0.08
left = max(0, left - pad)
top = max(0, top - pad)
right = min(1, right + pad)
bottom = min(1, bottom + pad)

# Crop in pixels
px1, py1 = int(left * W), int(top * H)
px2, py2 = int(right * W), int(bottom * H)
print(f"\n[Step 2] Cropping clock region: ({px1},{py1}) to ({px2},{py2})")

crop = img.crop((px1, py1, px2, py2))
crop.save("clock_crop.png")
print(f"Saved clock_crop.png ({crop.size[0]}x{crop.size[1]} pixels)")

# Now verify clock contents with 3 agents on the CROP
CROP_B64 = base64.b64encode(open("clock_crop.png", "rb").read()).decode("utf-8")

UNBIASED = """You are examining a cropped region from a Bitcoin puzzle image. It should contain a clock/dial.
Describe EXACTLY what you see:
1. How many clock hands?
2. What does each hand point to?
3. Any text labels ON or NEAR the hands? Quote them exactly.
4. Any text on the dial face?
5. Any numbers or Roman numerals?

Rules: Do NOT guess. If unclear, say "unclear". Quote text exactly as shown."""

results = {}

# Agent 1: Nemotron
print("\n[Agent 1: Nemotron] Analyzing crop...")
try:
    r, _ = swarm.vision(UNBIASED, image_path="clock_crop.png")
    if r: results["Nemotron"] = r; print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Agent 2: Qwen
print("[Agent 2: Qwen] Analyzing crop...")
try:
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    comp = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role":"user","content":[
            {"type":"text","text":UNBIASED},
            {"type":"image_url","image_url":{"url":f"data:image/png;base64,{CROP_B64}"}}
        ]}],
        max_tokens=1500, temperature=0.1
    )
    results["Qwen"] = comp.choices[0].message.content
    print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Agent 3: Gemini
print("[Agent 3: Gemini] Analyzing crop...")
try:
    from google import genai
    from google.genai import types
    gclient = genai.Client(api_key=GEMINI_KEY)
    with open("clock_crop.png","rb") as f:
        cb = f.read()
    resp = gclient.models.generate_content(
        model="gemini-3.6-flash",
        contents=[types.Part.from_bytes(data=cb, mime_type="image/png"), UNBIASED]
    )
    results["Gemini"] = resp.text
    print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Per-agent claim counting (FIXED logic - no M7 bug)
def agent_claims(text):
    claims = set()
    t = text.lower()
    if 'moon' in t: claims.add('MOON')
    if 'tower' in t: claims.add('TOWER')
    if 'food' in t: claims.add('FOOD')
    if '1865' in t: claims.add('1865')
    return claims

claim_agents = {}
for agent, resp in results.items():
    for c in agent_claims(resp):
        claim_agents.setdefault(c, []).append(agent)

print("\n" + "=" * 60)
print("INDIVIDUAL RESPONSES")
print("=" * 60)
for agent, resp in results.items():
    print(f"\n--- {agent} ---\n{resp}")

print("\n" + "=" * 60)
print("CORRECTED CONSENSUS (per agent)")
print("=" * 60)
for claim, agents in claim_agents.items():
    status = "CONFIRMED" if len(agents) >= 2 else "NOT CONFIRMED"
    print(f"  {claim}: {len(agents)}/{len(results)} {status} (by: {', '.join(agents)})")

# Save
swarm.save_to_kb("bnb_02btc", "clock_crop_analysis", {
    "bounding_box": {"left":left,"top":top,"right":right,"bottom":bottom},
    "crop_size": [crop.size[0], crop.size[1]],
    "responses": results,
    "consensus": {c: len(a) >= 2 for c, a in claim_agents.items()}
})
print("\nSaved to knowledge_base. Check swarm/clock_crop.png to see what was cropped.")