"""
MISSION: 3-Agent Vision Voting System (FIXED)
==============================================
Uses env vars directly (not swarm.groq_key which doesn't exist)
"""
import sys, os, json, base64
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator_v2 import Swarm

swarm = Swarm()

# Get keys directly from env
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

IMG_PATH = "blm.png"
if not os.path.exists(IMG_PATH):
    print(f"ERROR: {IMG_PATH} not found")
    sys.exit(1)

with open(IMG_PATH, "rb") as f:
    img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

print("=" * 70)
print("3-AGENT VISION VOTING SYSTEM")
print("=" * 70)
print(f"Image: {IMG_PATH} ({os.path.getsize(IMG_PATH)} bytes)")
print()

# UNBIASED prompt — no suggested content (prevents hallucination, M6)
UNBIASED_PROMPT = """You are examining a Bitcoin puzzle collage image.
Focus on the clock/dial region in the upper portion of the image.

Describe EXACTLY what you see:
1. How many clock hands are visible?
2. What number or position does each hand point to?
3. Are there any text labels visible near or on the clock hands?
4. What text (if any) is written on the dial face?
5. Are there any Roman numerals or numbers on the dial?

Rules:
- Do NOT guess or infer
- If you cannot clearly see something, write "unclear"
- List only what you can definitively read
- Output as plain text, one answer per numbered point"""

results = {}

# Agent 1: Nemotron (via orchestrator)
print("\n[Agent 1: Nemotron 12B VL] Querying...")
try:
    result, _ = swarm.vision(UNBIASED_PROMPT, image_path=IMG_PATH)
    if result:
        results["Nemotron 12B VL"] = result
        print(f"  ✓ Responded ({len(result)} chars)")
    else:
        print("  ✗ Returned None")
except Exception as e:
    print(f"  ✗ Failed: {str(e)[:100]}")

# Agent 2: Qwen (via Groq directly)
print("\n[Agent 2: Qwen 3.6 27B] Querying...")
try:
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    content = [
        {"type": "text", "text": UNBIASED_PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
    ]
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role": "user", "content": content}],
        max_tokens=2000,
        temperature=0.1
    )
    result = completion.choices[0].message.content
    if result:
        results["Qwen 3.6 27B"] = result
        print(f"  ✓ Responded ({len(result)} chars)")
except Exception as e:
    print(f"  ✗ Failed: {str(e)[:100]}")

# Agent 3: Gemini (via google.genai)
print("\n[Agent 3: Gemini 3.6 Flash] Querying...")
try:
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
            UNBIASED_PROMPT
        ]
    )
    result = response.text
    if result:
        results["Gemini 3.6 Flash"] = result
        print(f"  ✓ Responded ({len(result)} chars)")
except Exception as e:
    print(f"  ✗ Failed: {str(e)[:100]}")

# Show individual responses
print("\n" + "=" * 70)
print("INDIVIDUAL AGENT RESPONSES")
print("=" * 70)

for agent_name, response in results.items():
    print(f"\n--- {agent_name} ---")
    print(response)

# Consensus analysis
print("\n" + "=" * 70)
print("CONSENSUS ANALYSIS")
print("=" * 70)

def extract_claims(text):
    claims = []
    lines = text.lower().split('\n')
    for line in lines:
        if 'moon' in line: claims.append('MOON')
        if 'tower' in line: claims.append('TOWER')
        if 'food' in line: claims.append('FOOD')
        if '1865' in line: claims.append('1865')
        if '202' in line: claims.append('202?')
        if 'two hands' in line or '2 hands' in line or '2 clock' in line: claims.append('2_HANDS')
        if 'three hands' in line or '3 hands' in line or '3 clock' in line: claims.append('3_HANDS')
    return claims

all_claims = []
for agent_name, response in results.items():
    claims = extract_claims(response)
    all_claims.extend(claims)

claim_counts = Counter(all_claims)

print("\nClaim frequency across agents:")
for claim, count in claim_counts.most_common():
    status = "✓ CONSENSUS" if count >= 2 else "✗ SINGLE"
    print(f"  {claim}: {count}/{len(results)} {status}")

# Final verdict
print("\n" + "=" * 70)
print("FINAL VERDICT (2/3 consensus required)")
print("=" * 70)

consensus_claims = [claim for claim, count in claim_counts.items() if count >= 2]

if consensus_claims:
    print("\nConfirmed by 2+ agents:")
    for claim in consensus_claims:
        print(f"  ✓ {claim}")
else:
    print("\nNo consensus reached")

print("\nSpecific verification:")
print(f"  MOON: {'CONFIRMED' if claim_counts.get('MOON', 0) >= 2 else 'NOT CONFIRMED'} ({claim_counts.get('MOON', 0)}/{len(results)})")
print(f"  TOWER: {'CONFIRMED' if claim_counts.get('TOWER', 0) >= 2 else 'NOT CONFIRMED'} ({claim_counts.get('TOWER', 0)}/{len(results)})")
print(f"  FOOD: {'CONFIRMED' if claim_counts.get('FOOD', 0) >= 2 else 'NOT CONFIRMED'} ({claim_counts.get('FOOD', 0)}/{len(results)})")
print(f"  1865: {'CONFIRMED' if claim_counts.get('1865', 0) >= 2 else 'NOT CONFIRMED'} ({claim_counts.get('1865', 0)}/{len(results)})")

# Save to KB
voting_data = {
    "timestamp": "2026-08-23",
    "agents_used": list(results.keys()),
    "individual_responses": results,
    "claim_counts": dict(claim_counts),
    "consensus_claims": consensus_claims,
    "verdict": {
        "moon": claim_counts.get('MOON', 0) >= 2,
        "tower": claim_counts.get('TOWER', 0) >= 2,
        "food": claim_counts.get('FOOD', 0) >= 2,
        "1865": claim_counts.get('1865', 0) >= 2
    }
}

swarm.save_to_kb("bnb_02btc", "vision_voting_3agents", voting_data)

print("\nMission complete.")