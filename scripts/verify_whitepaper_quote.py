"""
Verify Bitcoin whitepaper quote on BLM dial
3-agent voting on the dial region ONLY
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

# Load the clock crop we made earlier
CROP_PATH = "clock_crop.png"
if not os.path.exists(CROP_PATH):
    print("ERROR: clock_crop.png not found")
    sys.exit(1)

with open(CROP_PATH, "rb") as f:
    crop_bytes = f.read()
    crop_b64 = base64.b64encode(crop_bytes).decode("utf-8")

print("=" * 70)
print("VERIFY BITCOIN WHITEPAPER QUOTE")
print("=" * 70)
print("Testing if dial contains: 'THEY WERE RECEIVED THE PAYEE NEEDS POOR...'")
print()

# FOCUSED PROMPT: only dial text
DIAL_PROMPT = """You are examining a cropped clock/dial region from a Bitcoin puzzle image.
Focus ONLY on the circular text written around the edge of the dial face.

1. Transcribe the text EXACTLY as it appears, word by word.
2. Is this text related to the Bitcoin whitepaper? (The Bitcoin whitepaper contains phrases about "payee", "transaction", "majority", "nodes")
3. Quote the EXACT text you see.

Rules:
- Do NOT guess or complete words
- If unclear, write [?]
- Output the text in reading order"""

results = {}

# Agent 1: Nemotron
print("[Agent 1: Nemotron] Reading dial text...")
try:
    r, _ = swarm.vision(DIAL_PROMPT, image_path=CROP_PATH)
    if r: results["Nemotron"] = r; print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Agent 2: Qwen
print("[Agent 2: Qwen] Reading dial text...")
try:
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    comp = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role":"user","content":[
            {"type":"text","text":DIAL_PROMPT},
            {"type":"image_url","image_url":{"url":f"data:image/png;base64,{crop_b64}"}}
        ]}],
        max_tokens=1500, temperature=0.1
    )
    results["Qwen"] = comp.choices[0].message.content
    print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Agent 3: Gemini
print("[Agent 3: Gemini] Reading dial text...")
try:
    from google import genai
    from google.genai import types
    gclient = genai.Client(api_key=GEMINI_KEY)
    resp = gclient.models.generate_content(
        model="gemini-3.6-flash",
        contents=[types.Part.from_bytes(data=crop_bytes, mime_type="image/png"), DIAL_PROMPT]
    )
    results["Gemini"] = resp.text
    print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Show individual responses
print("\n" + "=" * 70)
print("INDIVIDUAL DIAL TEXT READINGS")
print("=" * 70)
for agent, resp in results.items():
    print(f"\n--- {agent} ---")
    print(resp[:600])

# Check for whitepaper keywords
print("\n" + "=" * 70)
print("WHITEPAPER KEYWORD ANALYSIS")
print("=" * 70)

whitepaper_words = ["payee", "transaction", "majority", "nodes", "received", "proof", "time"]
for agent, resp in results.items():
    found = [w for w in whitepaper_words if w.lower() in resp.lower()]
    print(f"\n{agent}:")
    print(f"  Whitepaper keywords found: {found}")

# Check for the specific quote
quote_fragment = "they were received"
print(f"\nSearching for '{quote_fragment}':")
for agent, resp in results.items():
    if quote_fragment.lower() in resp.lower():
        print(f"  ✓ {agent} contains the quote")
    else:
        print(f"  ✗ {agent} does NOT contain the quote")

# Save results
swarm.save_to_kb("bnb_02btc", "whitepaper_quote_verification", {
    "timestamp": "2026-08-23",
    "hypothesis": "Dial contains Bitcoin whitepaper quote",
    "agents_used": list(results.keys()),
    "individual_responses": results,
    "quote_confirmed": any(quote_fragment.lower() in r.lower() for r in results.values()),
    "whitepaper_keywords_found": {
        agent: [w for w in whitepaper_words if w.lower() in resp.lower()]
        for agent, resp in results.items()
    }
})

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)