"""
Convert cipher Greek numerals to BIP39 words
H2 hypothesis: [15,4,13,13,4], [4,8,4,24], [700,4,15,4,9]
"""
import json
from pathlib import Path

# Load BIP39 wordlist
bip39_path = Path("../knowledge_base/bip39_english.txt")
words = open(bip39_path).read().splitlines()

print("=" * 70)
print("CIPHER → BIP39 CONVERSION")
print("=" * 70)

# Cipher groups as Greek numerals (H2 hypothesis)
groups = {
    "Group 1 (OΔMMΔ)": [15, 4, 13, 13, 4],
    "Group 2 (48ΔX)": [4, 8, 4, 24],
    "Group 3 (Ψ4O4I)": [700, 4, 15, 4, 9]
}

# Convert to words (0-indexed)
all_words = []
for group_name, indices in groups.items():
    print(f"\n{group_name}:")
    print(f"  Indices: {indices}")
    group_words = [words[i-1] for i in indices if 1 <= i <= len(words)]
    print(f"  Words: {group_words}")
    all_words.extend(group_words)

print(f"\n{'=' * 70}")
print(f"ALL {len(all_words)} WORDS:")
print(f"{'=' * 70}")
for i, word in enumerate(all_words, 1):
    print(f"  {i}. {word}")

# Check if any are in core9
print(f"\n{'=' * 70}")
print("OVERLAP WITH KNOWN CORE9:")
print(f"{'=' * 70}")
core9 = ["moon", "tower", "food", "black", "this", "subject", "one", "order", "real"]
for word in all_words:
    if word in core9:
        print(f"  ✓ {word} is in core9")

# Test 12-word combinations
print(f"\n{'=' * 70}")
print("POSSIBLE 12-WORD SEED PHRASES:")
print(f"{'=' * 70}")
print(f"Total words: {len(all_words)}")
print(f"Need: 12 words + checksum")

# Option 1: First 12 words
if len(all_words) >= 12:
    print(f"\nOption 1 (first 12):")
    for i, word in enumerate(all_words[:12], 1):
        print(f"  {i}. {word}")

# Option 2: Last 12 words
print(f"\nOption 2 (last 12):")
for i, word in enumerate(all_words[-12:], 1):
    print(f"  {i}. {word}")

# Save results
results = {
    "cipher": "OΔMMΔ:48ΔX:Ψ4O4I",
    "hypothesis": "Greek numerals → BIP39 indices",
    "groups": groups,
    "words": all_words,
    "total_words": len(all_words),
    "core9_overlap": [w for w in all_words if w in core9]
}

# Save to KB
from dotenv import load_dotenv
import sys, os
load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator_v2 import Swarm
swarm = Swarm()
swarm.save_to_kb("bnb_02btc", "cipher_bip39_words", results)

print(f"\n{'=' * 70}")
print("Saved to knowledge_base.")
print(f"{'=' * 70}")