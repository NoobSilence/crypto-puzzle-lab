"""
Test google.genai SDK with CURRENT models (not deprecated)
DATA-FIRST: try gemini-3.6-flash first (newest free model)
"""
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("ERROR: GEMINI_API_KEY not in .env")
    exit(1)

try:
    from google import genai
    client = genai.Client(api_key=GEMINI_KEY)
    
    # Try models in order: newest first (aug 2026)
    models_to_try = [
        "gemini-3.6-flash",      # current free tier
        "gemini-3.7-flash",      # latest (aug 2026)
        "gemini-2.5-flash-lite", # older but may still work
    ]
    
    for model_name in models_to_try:
        try:
            print(f"Trying {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents="Say OK if you work"
            )
            print(f"SUCCESS with {model_name}!")
            print(f"Response: {response.text}")
            
            # Save working model to config
            import json
            config_path = "gemini_config.json"
            config = {"working_model": model_name, "sdk": "google.genai"}
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            print(f"Saved to {config_path}")
            exit(0)
            
        except Exception as e:
            print(f"  Failed: {str(e)[:150]}")
    
    print("\nAll Gemini models failed - we'll use 2-agent voting")
    
except Exception as e:
    print("SDK import failed:", str(e)[:200])