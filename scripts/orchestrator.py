"""Backward-compatible import surface for the v2 swarm orchestrator."""
from orchestrator_v2 import Swarm as _Swarm


class Swarm(_Swarm):
    """Keep the v1 method names while using the maintained v2 implementation."""

    def __init__(self):
        super().__init__()
        from orchestrator_v2 import GEMINI_KEY, GROQ_KEY

        self.gemini_key = GEMINI_KEY
        self.groq_key = GROQ_KEY

    def vision_agent(self, task: str, image_path: str = None) -> str:
        result, _ = self.vision(task, image_path=image_path)
        return result

    def reason_agent(self, task: str) -> str:
        result, _ = self.reason(task)
        return result

if __name__ == "__main__":
    swarm = Swarm()
    print("Swarm online.")
    print(f"  Gemini: {'OK' if swarm.gemini_key else 'MISSING'}")
    print(f"  Groq:   {'OK' if swarm.groq_key else 'MISSING'}")
