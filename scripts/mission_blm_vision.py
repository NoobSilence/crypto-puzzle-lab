"""BLM collage forensic transcription using the maintained swarm orchestrator."""
import sys, os, requests, base64, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator_v2 import Swarm

swarm = Swarm()

IMG_URL = "https://raw.githubusercontent.com/floflo777/open-crypto-puzzles/main/1-big-prizes/blm-brave-new-world-0-2btc/clues/welcome-to-the-brave-new-world.png"
IMG_LOCAL = "blm.png"

# 1) Download image
if not os.path.exists(IMG_LOCAL):
    print("Downloading BLM image...")
    r = requests.get(IMG_URL, timeout=30)
    r.raise_for_status()
    open(IMG_LOCAL, "wb").write(r.content)
    print("OK image:", len(r.content), "bytes")
else:
    print("Image already present:", os.path.getsize(IMG_LOCAL), "bytes")

# 2) Convert naar base64
print("Converting image to base64...")
with open(IMG_LOCAL, "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

# 3) Groq Vision - Qwen 3.6 27B (het enige vision model)
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TASK = """You are a forensic image analyst examining a Bitcoin puzzle collage.
Transcribe EVERY visible text element, region by region:
(1) Statue of Liberty PEDESTAL engraving - every character, exact as-is
(2) BOTTOM BAND text (if any) - every character  
(3) DIAL/CLOCK region - labels, pointer positions, any text or numbers
(4) RIGHT-EDGE glyph column - describe shapes, count them
(5) LIST all recognizable English words anywhere in the image

Output ONLY valid JSON with this exact structure:
{
  "pedestal": {"text": "...", "confidence": 0.0},
  "bottom_band": {"text": "...", "confidence": 0.0},
  "dial": {"text": "...", "confidence": 0.0},
  "glyphs": {"count": 0, "description": "..."},
  "words_found": ["word1", "word2"],
  "bip39_candidates": ["word1", "word2"]
}

Rules:
- confidence is 0.0-1.0
- Do NOT invent text. Use "[?]" for uncertain characters
- Return ONLY the JSON, no markdown or explanation"""

print("Running Groq Vision (qwen/qwen3.6-27b)...")
try:
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": TASK},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        max_completion_tokens=4000,
        response_format={"type": "json_object"}
    )
    result = completion.choices[0].message.content
    print("SUCCESS with model: qwen/qwen3.6-27b")
except Exception as e:
    print("Groq Vision failed:", str(e)[:300])
    sys.exit(1)

print("\n=== VISION OUTPUT ===")
print(result)

# Parse JSON en valideer
try:
    parsed = json.loads(result)
    print("\n=== PARSED JSON ===")
    print(json.dumps(parsed, indent=2))
    swarm.save_to_kb("bnb_02btc", "vision_transcript", parsed)
    print("\nMISSIE 1 COMPLETE - saved to knowledge_base")
except json.JSONDecodeError as e:
    print("\nJSON parse failed:", e)
    print("Raw output saved as string")
    swarm.save_to_kb("bnb_02btc", "vision_transcript", result)