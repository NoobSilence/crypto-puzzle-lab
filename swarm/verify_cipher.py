"""
Verify cipher string on clock dial
Focus ONLY on dial text, not hands
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

# Load the clock crop we just made
CROP_PATH = "clock_crop.png"
if not os.path.exists(CROP_PATH):
    print("ERROR: clock_crop.png not found. Run auto_find_clock.py first.")
    sys.exit(1)

img = Image.open(CROP_PATH)
W, H = img.size
print(f"Clock crop: {W}x{H} pixels")

with open(CROP_PATH, "rb") as f:
    crop_bytes = f.read()
    crop_b64 = base64.b64encode(crop_bytes).decode("utf-8")

# FOCUSED PROMPT: only dial text, not hands
DIAL_PROMPT = """You are examining a cropped clock/dial region from a Bitcoin puzzle image.
Focus ONLY on the text/symbols written ON THE DIAL FACE ITSELF (not on the hands).

Look for:
1. Any text strings (English, Latin, cipher, runes)
2. Any symbols (Greek letters, runic characters, cipher glyphs)
3. Any numbers or codes

If you see a string like "OΔMMΔ:48ΔX:Ψ4O4I" or similar cipher/runes, quote it EXACTLY.
If you see NO text on the dial, say "No text visible on dial face."
Do NOT describe the clock hands. Focus only on the dial surface."""

results = {}

# Agent 1: Nemotron
print("\n[Agent 1: Nemotron] Analyzing dial text...")
try:
    r, _ = swarm.vision(DIAL_PROMPT, image_path=CROP_PATH)
    if r: results["Nemotron"] = r; print("  OK")
except Exception as e: print(f"  Failed: {e}")

# Agent 2: Qwen
print("[Agent 2: Qwen] Analyzing dial text...")
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
print("[Agent 3: Gemini] Analyzing dial text...")
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

# Per-agent analysis
print("\n" + "=" * 60)
print("INDIVIDUAL DIAL ANALYSIS")
print("=" * 60)
for agent, resp in results.items():
    print(f"\n--- {agent} ---")
    print(resp[:800])

# Check for cipher string mentions
print("\n" + "=" * 60)
print("CIPHER STRING VERIFICATION")
print("=" * 60)

cipher_variants = []
for agent, resp in results.items():
    if 'oδ' in resp.lower() or 'cipher' in resp.lower() or 'rune' in resp.lower():
        cipher_variants.append((agent, resp))
        print(f"\n{agent} mentions cipher/runes:")
        # Extract relevant lines
        for line in resp.split('\n'):
            if any(k in line.lower() for k in ['cipher', 'rune', 'symbol', 'oδ', 'text']):
                print(f"  {line[:200]}")

if not cipher_variants:
    print("\nNo agent mentions cipher string on dial")

# Save
swarm.save_to_kb("bnb_02btc", "dial_cipher_verification", {
    "responses": results,
    "cipher_mentioned": len(cipher_variants) > 0,
    "agents_with_cipher": [a for a, _ in cipher_variants]
})

print("\nSaved to knowledge_base.")