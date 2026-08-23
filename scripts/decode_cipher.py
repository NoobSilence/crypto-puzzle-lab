"""
Decode cipher string: OΔMMΔ:48ΔX:Ψ4O4I
Test multiple hypotheses automatically
"""
import json
from pathlib import Path

CIPHER = "OΔMMΔ:48ΔX:Ψ4O4I"
groups = CIPHER.split(":")

print("=" * 70)
print("CIPHER DECODER: " + CIPHER)
print("=" * 70)

# Hypothesis 1: Letter position (A=1, B=2, ...)
print("\n[H1] Letter position (A=1, B=2, ...)")
def letter_pos(char):
    if char.isalpha():
        return ord(char.upper()) - ord('A') + 1
    return None

for i, group in enumerate(groups):
    positions = [letter_pos(c) for c in group if c.isalpha()]
    print(f"  Group {i+1}: {group} → positions {positions}")

# Hypothesis 2: Greek numerals
print("\n[H2] Greek numeral values")
greek_nums = {'Δ': 4, 'Ξ': 60, 'Ψ': 700, 'Ω': 800}
for i, group in enumerate(groups):
    values = []
    for c in group:
        if c in greek_nums:
            values.append(f"{c}={greek_nums[c]}")
        elif c.isdigit():
            values.append(c)
        elif c.isalpha():
            values.append(f"{c}={letter_pos(c)}")
    print(f"  Group {i+1}: {group} → {values}")

# Hypothesis 3: Roman numeral interpretation
print("\n[H3] Roman numeral interpretation")
roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
for i, group in enumerate(groups):
    roman_values = [roman_map.get(c, None) for c in group if c in roman_map]
    if roman_values:
        print(f"  Group {i+1}: {group} → Roman values {roman_values}")

# Hypothesis 4: Mixed encoding (numbers + letters)
print("\n[H4] Mixed encoding (preserve numbers, convert letters)")
for i, group in enumerate(groups):
    mixed = []
    for c in group:
        if c.isdigit():
            mixed.append(int(c))
        elif c.isalpha():
            mixed.append(letter_pos(c))
        else:
            mixed.append(c)
    print(f"  Group {i+1}: {group} → {mixed}")

# Hypothesis 5: BIP39 wordlist test (if we have wordlist)
print("\n[H5] BIP39 wordlist test")
bip39_path = Path("../knowledge_base/bip39_english.txt")
if bip39_path.exists():
    words = open(bip39_path).read().splitlines()
    print(f"  BIP39 wordlist loaded: {len(words)} words")
    
    # Test letter positions as word indices (1-based)
    all_positions = []
    for group in groups:
        for c in group:
            pos = letter_pos(c)
            if pos and 1 <= pos <= len(words):
                all_positions.append((pos, words[pos-1]))
    
    print(f"  Possible BIP39 words from letter positions:")
    for pos, word in all_positions[:20]:  # Show first 20
        print(f"    Position {pos}: {word}")
else:
    print("  BIP39 wordlist not found - downloading...")
    # Download BIP39 wordlist
    import urllib.request
    url = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt"
    try:
        urllib.request.urlretrieve(url, bip39_path)
        words = open(bip39_path).read().splitlines()
        print(f"  Downloaded: {len(words)} words")
        
        all_positions = []
        for group in groups:
            for c in group:
                pos = letter_pos(c)
                if pos and 1 <= pos <= len(words):
                    all_positions.append((pos, words[pos-1]))
        
        print(f"  Possible BIP39 words from letter positions:")
        for pos, word in all_positions[:20]:
            print(f"    Position {pos}: {word}")
    except Exception as e:
        print(f"  Download failed: {e}")

# Hypothesis 6: Date/time parsing
print("\n[H6] Date/time interpretation")
print("  If 48 = minutes, ΔX = 10:48 (Δ=4 in Greek, X=10 in Roman)")
print("  If Ψ4O4I = encoded time: Ψ=700, 4=4, O=15, 4=4, I=1")

# Save results
results = {
    "cipher": CIPHER,
    "groups": groups,
    "hypotheses": {
        "letter_positions": [[letter_pos(c) for c in g if c.isalpha()] for g in groups],
        "greek_values": [{c: greek_nums.get(c, None) for c in g if c in greek_nums} for g in groups],
        "mixed_encoding": [[int(c) if c.isdigit() else letter_pos(c) for c in g] for g in groups]
    }
}

# Save to KB
from dotenv import load_dotenv
import sys, os
load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator_v2 import Swarm
swarm = Swarm()
swarm.save_to_kb("bnb_02btc", "cipher_decoding_attempts", results)

print("\n" + "=" * 70)
print("Decoding complete. Results saved to knowledge_base.")
print("=" * 70)