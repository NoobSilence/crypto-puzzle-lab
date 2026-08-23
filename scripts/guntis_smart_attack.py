"""
Guntis 10 ETH - Smart Brute Force Attack
=========================================
Target: 0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF
Path: m/44'/60'/0'/0/0 (MetaMask standard, no passphrase)

Confirmed anchors (from floflo777's folder):
  Position 1 (index 0): "dutch"
  Position 5 (index 4): "fog"
  Position 12 (index 11): "parrot"

Unplaced words (confirmed):
  "fiber" (from video 03wXiMczCXk @ 15:26)
  "fork" (from video ZjBJKooVmuE @ 17:28)

Hint words for remaining 7 positions:
  will, only, like, round (from metadata/connecting words)

Strategy:
  1. Fix anchors: dutch(1), fog(5), parrot(12)
  2. Permute fiber + fork across 9 available positions
  3. Fill remaining 7 positions with hint words
  4. BIP39 checksum pre-filter (fast, pure Python)
  5. ETH derivation only for checksum-valid candidates
  6. Compare against target
"""
import sys
import os
import time
from itertools import permutations, product
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check dependencies
try:
    from mnemonic import Mnemonic
    from eth_account import Account
    from eth_utils import to_checksum_address
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install: pip install mnemonic eth-account eth-utils")
    sys.exit(1)

# Configuration
TARGET = "0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF"
DERIVATION_PATH = "m/44'/60'/0'/0/0"

# Anchors (0-indexed positions)
ANCHORS = {
    0: "dutch",      # Position 1: Netherlands
    4: "fog",        # Position 5: condensed droplets
    11: "parrot"     # Position 12: tropical bird
}

# Unplaced words (must be placed in available positions)
UNPLACED = ["fiber", "fork"]

# Hint words from metadata (floflo777's folder)
HINT_WORDS = ["will", "only", "like", "round"]

# All available positions (not anchored)
AVAILABLE = [i for i in range(12) if i not in ANCHORS]

print("=" * 70)
print("GUNTIS 10 ETH - SMART BRUTE FORCE")
print("=" * 70)
print(f"Target: {TARGET}")
print(f"Path: {DERIVATION_PATH}")
print(f"Anchors: {ANCHORS}")
print(f"Unplaced: {UNPLACED}")
print(f"Hint words for remaining: {HINT_WORDS}")
print("=" * 70)

# Initialize
mnemo = Mnemonic("english")
wordlist = mnemo.wordlist

# Validate all words are BIP39
all_words = list(ANCHORS.values()) + UNPLACED + HINT_WORDS
for word in all_words:
    if word not in wordlist:
        print(f"ERROR: '{word}' is not a BIP39 word!")
        sys.exit(1)

print(f"\n[Setup] All {len(all_words)} words validated as BIP39")

# Generate fiber/fork permutations
unplaced_perms = list(permutations(AVAILABLE, len(UNPLACED)))
print(f"[Setup] fiber/fork permutations: {len(unplaced_perms)}")

def get_remaining_positions(perm):
    """Get positions not filled by anchors or fiber/fork"""
    filled = set(ANCHORS.keys()) | set(perm)
    return [i for i in range(12) if i not in filled]

# Test first permutation structure
first_remaining = get_remaining_positions(unplaced_perms[0])
print(f"[Setup] Remaining positions per permutation: {len(first_remaining)}")

# Calculate search space
hint_count = len(HINT_WORDS)
remaining_count = len(first_remaining)
combos_per_perm = hint_count ** remaining_count
total_combos = len(unplaced_perms) * combos_per_perm
print(f"[Setup] Combos per permutation: {combos_per_perm:,}")
print(f"[Setup] Total combinations: {total_combos:,}")
print(f"[Setup] Estimated checksum-valid: ~{total_combos // 16:,}")

def save_to_kb(key, data):
    """Save to knowledge base with error handling"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        from orchestrator_v2 import Swarm
        swarm = Swarm()
        swarm.save_to_kb("guntis_10eth", key, data)
        return True
    except Exception as e:
        print(f"  [Save warning] Could not save: {e}")
        return False

def derive_address(mnemonic_str):
    """Derive ETH address from mnemonic"""
    try:
        account = Account.from_mnemonic(mnemonic_str, account_path=DERIVATION_PATH)
        return to_checksum_address(account.address)
    except Exception:
        return None

# Statistics
tested = 0
checksum_valid = 0
hits = 0
start_time = time.time()

print("\n[Attack] Starting smart brute force...")
print(f"[Attack] This may take several hours. Progress updates every 1000 tests.")
print(f"[Attack] Press Ctrl+C to save checkpoint and stop.\n")

try:
    for perm_idx, perm in enumerate(unplaced_perms):
        # Build base word list with anchors + fiber/fork
        words = [""] * 12
        for pos, word in ANCHORS.items():
            words[pos] = word
        for pos, word in zip(perm, UNPLACED):
            words[pos] = word
        
        remaining_pos = get_remaining_positions(perm)
        
        # Iterate through all hint word combinations for remaining positions
        for combo in product(HINT_WORDS, repeat=len(remaining_pos)):
            test_words = words.copy()
            for pos, word in zip(remaining_pos, combo):
                test_words[pos] = word
            
            tested += 1
            
            # BIP39 checksum pre-filter (fast, pure Python)
            mnemonic_str = " ".join(test_words)
            if not mnemo.check(mnemonic_str):
                continue
            
            checksum_valid += 1
            
            # Only derive address for checksum-valid candidates
            derived = derive_address(mnemonic_str)
            if derived and derived.lower() == TARGET.lower():
                hits += 1
                print("\n" + "!" * 70)
                print("!!! HIT FOUND !!!")
                print("!" * 70)
                print(f"Mnemonic: {mnemonic_str}")
                print(f"Address: {derived}")
                print("!" * 70)
                
                save_to_kb("HIT_FOUND", {
                    "mnemonic": mnemonic_str,
                    "address": derived,
                    "path": DERIVATION_PATH,
                    "target": TARGET,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                sys.exit(0)
            
            # Progress reporting
            if tested % 1000 == 0:
                elapsed = time.time() - start_time
                rate = tested / elapsed if elapsed > 0 else 0
                if rate > 0:
                    eta_hours = ((total_combos - tested) / rate) / 3600
                else:
                    eta_hours = 0
                print(f"  Tested: {tested:,}/{total_combos:,} "
                      f"({tested/total_combos*100:.2f}%) | "
                      f"Checksum valid: {checksum_valid:,} | "
                      f"Rate: {rate:.0f}/sec | "
                      f"ETA: {eta_hours:.1f}h")

except KeyboardInterrupt:
    print("\n\n[Interrupted] Saving checkpoint...")
    elapsed = time.time() - start_time
    save_to_kb("smart_attack_checkpoint", {
        "tested": tested,
        "checksum_valid": checksum_valid,
        "elapsed_seconds": elapsed,
        "status": "interrupted - resume needed"
    })
    print(f"  Tested: {tested:,} | Checksum valid: {checksum_valid:,}")
    sys.exit(0)

# Final report
elapsed = time.time() - start_time
print("\n" + "=" * 70)
print("ATTACK COMPLETE - NO HIT FOUND")
print("=" * 70)
print(f"  Total tested: {tested:,}")
print(f"  Checksum valid: {checksum_valid:,}")
print(f"  Elapsed: {elapsed/3600:.2f} hours")
print(f"  Rate: {tested/elapsed:.0f}/sec")

save_to_kb("smart_attack_result", {
    "tested": tested,
    "checksum_valid": checksum_valid,
    "hits": hits,
    "elapsed_seconds": elapsed,
    "status": "complete - no hit"
})
print("  Results saved to knowledge base")