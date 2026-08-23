"""
Discover available FREE models on OpenRouter
DATA-FIRST: verify what actually works before building orchestrator
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("ERROR: OPENROUTER_API_KEY not found in .env")
    exit(1)

# 1) Get all models
print("Fetching model list from OpenRouter...")
response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

if response.status_code != 200:
    print(f"ERROR: {response.status_code} - {response.text}")
    exit(1)

models = response.json()["data"]
print(f"Total models available: {len(models)}")

# 2) Filter FREE models
free_models = [m for m in models if m["pricing"]["prompt"] == "0" and m["pricing"]["completion"] == "0"]
print(f"FREE models: {len(free_models)}")

# 3) Categorize by capability
vision = []
reasoning = []
coding = []
multimodal = []

for m in free_models:
    name = m["id"]
    desc = m.get("description", "").lower()
    
    if any(k in name.lower() for k in ["vision", "vl", "omni", "image"]):
        vision.append(name)
    if any(k in name.lower() for k in ["nemotron", "glm", "ox", "reason"]):
        reasoning.append(name)
    if any(k in name.lower() for k in ["code", "laguna", "codestral"]):
        coding.append(name)
    if any(k in name.lower() for k in ["omni", "multimodal", "vision"]):
        multimodal.append(name)

print("\n=== VISION/MULTIMODAL (free) ===")
for m in vision[:10]:
    print(f"  {m}")

print("\n=== REASONING (free) ===")
for m in reasoning[:10]:
    print(f"  {m}")

print("\n=== CODING (free) ===")
for m in coding[:10]:
    print(f"  {m}")

print("\n=== MULTIMODAL (free) ===")
for m in multimodal[:10]:
    print(f"  {m}")

# 4) Save to config for orchestrator
import json
config = {
    "vision": vision[:5],
    "reasoning": reasoning[:5],
    "coding": coding[:5],
    "multimodal": multimodal[:5],
    "total_free_models": len(free_models)
}

with open("free_models_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("\nConfig saved to free_models_config.json")
print("Next: build orchestrator using these verified models")