"""
Verify clock/dial reading with unbiased prompt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator_v2 import Swarm

swarm = Swarm()

UNBIASED_TASK = """You are examining a Bitcoin puzzle collage.
Focus on the clock/dial in the upper portion.

Describe EXACTLY what you see:
1. How many clock hands are visible?
2. What does each hand point to (number or symbol)?
3. Are there any text labels ON the hands themselves (not pointing to them)?
4. What text (if any) is written on the dial face?
5. Are there Roman numerals?

Do NOT guess. If you cannot clearly see something, say "unclear".
Output as simple text, not JSON."""

result, model = swarm.vision(UNBIASED_TASK, image_path="blm.png")

if result:
    print("UNBIASED VISION OUTPUT:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    swarm.save_to_kb("bnb_02btc", "clock_verification", result)
else:
    print("Vision failed")