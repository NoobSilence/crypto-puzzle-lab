"""
Verify which free models ACTUALLY work (not just listed)
DATA-FIRST: test before building orchestrator
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

def test_openrouter(model_id):
    """Test if OpenRouter model responds"""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": "Say OK"}],
                "max_tokens": 10
            },
            timeout=15
        )
        if response.status_code == 200:
            return {"status": "OK", "model": model_id}
        else:
            return {"status": "FAIL", "model": model_id, "error": response.status_code}
    except Exception as e:
        return {"status": "ERROR", "model": model_id, "error": str(e)[:100]}

def test_groq_vision():
    """Test Groq qwen3.6-27b vision"""
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_KEY)
        completion = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=10
        )
        return {"status": "OK", "model": "qwen/qwen3.6-27b", "source": "groq"}
    except Exception as e:
        return {"status": "FAIL", "model": "qwen/qwen3.6-27b", "error": str(e)[:100]}

def test_ollama():
    """Test local Ollama gemma3:4b"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:4b",
                "prompt": "Say OK",
                "stream": False
            },
            timeout=10
        )
        if response.status_code == 200:
            return {"status": "OK", "model": "gemma3:4b", "source": "ollama"}
        else:
            return {"status": "FAIL", "model": "gemma3:4b", "error": response.status_code}
    except Exception as e:
        return {"status": "ERROR", "model": "gemma3:4b", "error": str(e)[:100]}

print("Testing models...")
print("=" * 60)

results = []

# 1) OpenRouter: vision
print("\n[Vision] Testing OpenRouter models...")
vision_models = [
    "nvidia/nemotron-nano-12b-v2-vl:free"
]
for model in vision_models:
    print(f"  Testing {model}...")
    results.append(test_openrouter(model))

# 2) OpenRouter: reasoning
print("\n[Reasoning] Testing OpenRouter models...")
reasoning_models = [
    "z-ai/glm-5.2:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-super-120b-a12b:free"
]
for model in reasoning_models:
    print(f"  Testing {model}...")
    results.append(test_openrouter(model))

# 3) OpenRouter: coding
print("\n[Coding] Testing OpenRouter models...")
coding_models = [
    "poolside/laguna-s-2.1:free",
    "cohere/north-mini-code:free"
]
for model in coding_models:
    print(f"  Testing {model}...")
    results.append(test_openrouter(model))

# 4) Groq: vision (fallback)
print("\n[Vision] Testing Groq qwen3.6-27b...")
results.append(test_groq_vision())

# 5) Ollama: local
print("\n[Local] Testing Ollama gemma3:4b...")
results.append(test_ollama())

# Summary
print("\n" + "=" * 60)
print("VERIFICATION RESULTS")
print("=" * 60)

working = [r for r in results if r["status"] == "OK"]
failed = [r for r in results if r["status"] != "OK"]

print(f"\n✓ Working models: {len(working)}")
for r in working:
    print(f"  {r['model']}")

print(f"\n✗ Failed models: {len(failed)}")
for r in failed:
    print(f"  {r['model']}: {r.get('error', 'unknown')}")

# Save results
with open("verified_models.json", "w") as f:
    json.dump({"working": working, "failed": failed}, f, indent=2)

print(f"\nResults saved to verified_models.json")
print(f"Next: build orchestrator using {len(working)} verified models")