"""
Swarm Orchestrator — Collectieve Eenheid
Jij = Commander | Ik = Orchestrator | Agents = Workers
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Swarm:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.kb_path = Path("../knowledge_base")
        self.log_path = Path("swarm.log")

    def vision_agent(self, task: str, image_path: str = None) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_key)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        if image_path:
            import PIL.Image
            img = PIL.Image.open(image_path)
            response = model.generate_content([task, img])
        else:
            response = model.generate_content(task)
        self._log("VISION", task[:50], response.text[:100])
        return response.text

    def reason_agent(self, task: str) -> str:
        from groq import Groq
        client = Groq(api_key=self.groq_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a cryptanalysis expert. Reason step-by-step."},
                {"role": "user", "content": task}
            ],
            temperature=0.2,
            max_tokens=4000
        )
        result = completion.choices[0].message.content
        self._log("REASON", task[:50], result[:100])
        return result

    def _log(self, agent, input_short, output_short):
        with open(self.log_path, "a", encoding="utf-8") as f:
            from datetime import datetime
            f.write(f"[{datetime.now().isoformat()}] [{agent}] {input_short} -> {output_short}\n")

    def save_to_kb(self, puzzle_id: str, key: str, value):
        path = self.kb_path / f"{puzzle_id}.json"
        data = json.load(open(path)) if path.exists() else {}
        data[key] = value
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to KB: {puzzle_id}.json[{key}]")

if __name__ == "__main__":
    swarm = Swarm()
    print("Swarm online.")
    print(f"  Gemini: {'OK' if swarm.gemini_key else 'MISSING'}")
    print(f"  Groq:   {'OK' if swarm.groq_key else 'MISSING'}")
