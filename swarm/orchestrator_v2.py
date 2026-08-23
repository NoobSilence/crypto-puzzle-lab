"""
Swarm Orchestrator v2.0 - Collective Unity
==========================================
5 verified agents with automatic fallback.
Built on DATA-FIRST evidence from verify_models.py (2026-08-23)

Architecture:
  [COMMANDER = human]
        |
  [ORCHESTRATOR = AI core]
    /    |     |      \      \
VISION REASON CODE   LOCAL  RESEARCH
"""
import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ============ CONFIGURATION ============
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

KB_PATH = Path(__file__).parent.parent / "knowledge_base"
LOG_PATH = Path(__file__).parent / "swarm.log"

# Verified models (from verify_models.py, 2026-08-23)
AGENTS = {
    "vision": [
        {"id": "nvidia/nemotron-nano-12b-v2-vl:free", "source": "openrouter"},
        {"id": "qwen/qwen3.6-27b", "source": "groq"},
    ],
    "reasoning": [
        {"id": "nvidia/nemotron-3-ultra-550b-a55b:free", "source": "openrouter"},
        {"id": "nvidia/nemotron-3-super-120b-a12b:free", "source": "openrouter"},
    ],
    "coding": [
        {"id": "poolside/laguna-s-2.1:free", "source": "openrouter"},
        {"id": "cohere/north-mini-code:free", "source": "openrouter"},
    ],
    "local": [
        {"id": "gemma3:4b", "source": "ollama"},
    ],
}

# ============ CORE ORCHESTRATOR ============
class Swarm:
    def __init__(self):
        self.stats = {"calls": 0, "success": 0, "fallbacks": 0, "errors": 0}

    def _log(self, agent, model, status, note=""):
        line = f"[{datetime.now().isoformat()}] [{agent}] [{model}] [{status}] {note}"
        print(line)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def call_agent(self, role, task, image_b64=None, max_tokens=2000):
        """
        Call an agent with automatic fallback through the verified model list.
        Returns (response_text, model_used) or (None, None) if all fail.
        """
        if role not in AGENTS:
            self._log(role, "none", "ERROR", f"Unknown role: {role}")
            return None, None

        for attempt, model_cfg in enumerate(AGENTS[role]):
            self.stats["calls"] += 1
            if attempt > 0:
                self.stats["fallbacks"] += 1
            try:
                result = self._dispatch(model_cfg, task, image_b64, max_tokens)
                if result:
                    self.stats["success"] += 1
                    self._log(role, model_cfg["id"], "OK", f"attempt={attempt+1}")
                    return result, model_cfg["id"]
            except Exception as e:
                self.stats["errors"] += 1
                self._log(role, model_cfg["id"], "FAIL", str(e)[:120])
                time.sleep(1)

        self._log(role, "ALL", "EXHAUSTED", "no model responded")
        return None, None

    def _dispatch(self, cfg, task, image_b64, max_tokens):
        """Route to the correct API based on source."""
        source = cfg["source"]
        model_id = cfg["id"]

        if source == "openrouter":
            return self._call_openrouter(model_id, task, image_b64, max_tokens)
        elif source == "groq":
            return self._call_groq(model_id, task, image_b64, max_tokens)
        elif source == "ollama":
            return self._call_ollama(model_id, task, max_tokens)
        return None

    def _call_openrouter(self, model_id, task, image_b64, max_tokens):
        content = [{"type": "text", "text": task}]
        if image_b64:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_b64}"}
            })
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/NoobSilence/crypto-puzzle-lab",
                "X-Title": "CryptoPuzzleLab Swarm"
            },
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": content}],
                "max_tokens": max_tokens,
                "temperature": 0.1
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 429:
            raise Exception("rate limit (429)")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text[:100]}")

    def _call_groq(self, model_id, task, image_b64, max_tokens):
        from groq import Groq
        client = Groq(api_key=GROQ_KEY)
        content = [{"type": "text", "text": task}]
        if image_b64:
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_b64}"}
            })
        completion = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens,
            temperature=0.1
        )
        return completion.choices[0].message.content

    def _call_ollama(self, model_id, task, max_tokens):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_id, "prompt": task, "stream": False},
            timeout=120
        )
        if response.status_code == 200:
            return response.json().get("response", "")
        raise Exception(f"Ollama HTTP {response.status_code}")

    # ============ CONVENIENCE METHODS ============
    def vision(self, task, image_path=None):
        img_b64 = None
        if image_path:
            import base64
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")
        return self.call_agent("vision", task, image_b64=img_b64, max_tokens=3000)

    def reason(self, task):
        return self.call_agent("reasoning", task, max_tokens=4000)

    def code(self, task):
        return self.call_agent("coding", task, max_tokens=4000)

    def local(self, task):
        """Private local inference - use for strategy-sensitive data"""
        return self.call_agent("local", task, max_tokens=2000)

    def save_to_kb(self, puzzle_id, key, value):
        """Write agent output to knowledge base"""
        path = KB_PATH / f"{puzzle_id}.json"
        data = json.load(open(path, encoding="utf-8")) if path.exists() else {}
        data[key] = value
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to KB: {puzzle_id}.json[{key}]")

    def report(self):
        """Print session statistics"""
        print("\n" + "=" * 60)
        print("SWARM SESSION REPORT")
        print("=" * 60)
        for k, v in self.stats.items():
            print(f"  {k}: {v}")

# ============ SELF TEST ============
if __name__ == "__main__":
    print("=" * 60)
    print("Swarm Orchestrator v2.0 - Self Test")
    print("=" * 60)

    swarm = Swarm()

    tests = [
        ("vision", "Say OK if you work", None),
        ("reasoning", "Say OK if you work", None),
        ("coding", "Say OK if you work", None),
        ("local", "Say OK if you work", None),
    ]

    for role, task, img in tests:
        print(f"\n--- Testing {role.upper()} agent ---")
        result, model = swarm.call_agent(role, task, image_b64=img, max_tokens=20)
        if result:
            print(f"  Response: {result[:80]}")
            print(f"  Model: {model}")
        else:
            print(f"  FAILED - no model responded")

    swarm.report()