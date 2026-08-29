#!/usr/bin/env python3
"""
Bitcoin Movie Enigma - order-preserving 24-word subset generator (BIP39 checksum filtered)
Reconstructed from spec 2026-08-29. Deps: embit (wordlist only).
Usage: python movie_enigma_combo_generator.py [words_file] [-o out_file]
"""
import sys, hashlib, math
from itertools import combinations

try:
    from embit.bip39 import WORDLIST
except ImportError:
    from embit.wordlists.bip39 import WORDLIST

BIP39 = set(WORDLIST)

DEFAULT_WORDS = """hard, glory, alien, mad, motion, now, escape, goon,
sun, possible, ill, life, good, eye, river, warrior,
clock, hope, gravity, first, solar, blade, planet, ordinary,
bar, shark, boy, cream, matrix, story, ghost, soft,
shine, human"""

def load_words(path):
    text = open(path, encoding="utf-8").read() if path else DEFAULT_WORDS
    return [w.strip().lower() for w in text.replace(",", " ").split() if w.strip()]

def checksum_ok(indices):
    bits = 0
    for i in indices:
        bits = (bits << 11) | i
    entropy = (bits >> 8).to_bytes(32, "big")
    return hashlib.sha256(entropy).digest()[0] == (bits & 0xFF)

def main():
    args = sys.argv[1:]
    out, words_path, i = "candidates.txt", None, 0
    while i < len(args):
        if args[i] == "-o":
            out = args[i + 1]; i += 2
        else:
            words_path = args[i]; i += 1

    words = load_words(words_path)
    invalid = [w for w in words if w not in BIP39]
    valid = [w for w in words if w in BIP39]
    if invalid:
        print(f"[WARN] NOT in BIP39 (excluded): {invalid}")
    if len(valid) < 24:
        print("[FATAL] fewer than 24 valid words"); sys.exit(1)

    idx = {w: i for i, w in enumerate(WORDLIST)}
    combos = math.comb(len(valid), 24)
    print(f"[INFO] valid words: {len(valid)} | combinations: {combos:,} | expected valid: ~{combos // 256:,}")

    vi = [idx[w] for w in valid]
    emitted = tested = 0
    with open(out, "w", encoding="utf-8") as fh:
        for combo in combinations(range(len(valid)), 24):
            tested += 1
            if checksum_ok(tuple(vi[p] for p in combo)):
                fh.write(" ".join(valid[p] for p in combo) + "\n")
                emitted += 1
    print(f"[DONE] tested={tested:,} emitted={emitted:,}")

if __name__ == "__main__":
    main()
