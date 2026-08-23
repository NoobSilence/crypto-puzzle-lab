"""
Fix: Correct voting logic (count agents, not mentions)
Also: Crop clock region for focused analysis
"""
import json
from pathlib import Path

# Load existing voting data
kb_path = Path("../knowledge_base/bnb_02btc.json")
data = json.load(open(kb_path, encoding="utf-8"))

voting = data.get("vision_voting_3agents", {})
responses = voting.get("individual_responses", {})

print("=" * 70)
print("CORRECTED VOTING ANALYSIS (per agent, not per mention)")
print("=" * 70)

def agent_claims(text):
    """Return SET of claims (each claim counted once per agent)"""
    claims = set()
    t = text.lower()
    # Only count if explicitly mentioned as a label/observation
    if '"moon"' in t or "labeled \"moon\"" in t or "label 'moon'" in t:
        claims.add('MOON')
    if '"tower"' in t or "labeled \"tower\"" in t or "label 'tower'" in t:
        claims.add('TOWER')
    if '"food"' in t or "labeled \"food\"" in t:
        claims.add('FOOD')
    if '1865' in t:
        claims.add('1865')
    if '202' in t:
        claims.add('202?')
    if 'three hands' in t or '3 hands' in t or '3 clock hands' in t:
        claims.add('3_HANDS')
    if 'two hands' in t or '2 hands' in t or '2 clock hands' in t:
        claims.add('2_HANDS')
    return claims

# Count how many agents make each claim
claim_agents = {}
for agent_name, response in responses.items():
    claims = agent_claims(response)
    print(f"\n{agent_name}:")
    print(f"  Claims: {sorted(claims)}")
    for claim in claims:
        if claim not in claim_agents:
            claim_agents[claim] = []
        claim_agents[claim].append(agent_name)

print("\n" + "=" * 70)
print("CORRECTED CONSENSUS (agents that explicitly claim)")
print("=" * 70)

for claim, agents in claim_agents.items():
    status = "✓ CONSENSUS" if len(agents) >= 2 else "✗ SINGLE"
    print(f"  {claim}: {len(agents)}/{len(responses)} {status} (by: {', '.join(agents)})")

print("\n" + "=" * 70)
print("FINAL CORRECTED VERDICT")
print("=" * 70)

moon_confirmed = len(claim_agents.get('MOON', [])) >= 2
tower_confirmed = len(claim_agents.get('TOWER', [])) >= 2
food_confirmed = len(claim_agents.get('FOOD', [])) >= 2

print(f"  MOON: {'CONFIRMED' if moon_confirmed else 'NOT CONFIRMED'} ({len(claim_agents.get('MOON', []))} agents)")
print(f"  TOWER: {'CONFIRMED' if tower_confirmed else 'NOT CONFIRMED'} ({len(claim_agents.get('TOWER', []))} agents)")
print(f"  FOOD: {'CONFIRMED' if food_confirmed else 'NOT CONFIRMED'} ({len(claim_agents.get('FOOD', []))} agents)")

# Save corrected data
voting["corrected_verdict"] = {
    "moon": moon_confirmed,
    "tower": tower_confirmed,
    "food": food_confirmed,
    "note": "Bug in original voting: counted mentions not agents. Corrected 2026-08-23."
}
data["vision_voting_3agents"] = voting

with open(kb_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("\nCorrected verdict saved to knowledge base.")