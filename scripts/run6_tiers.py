import time
from itertools import permutations
import multiprocessing as mp
from embit import bip39, bip32
from coincurve import PublicKey
from Crypto.Hash import keccak

TARGET = "0x9c2f44efad0c1e852a09df9939e6daf061140caf"
PATH = "m/44'/60'/0'/0/0"
ANCHORS = {0: "dutch", 4: "fog", 11: "parrot"}
UNPLACED = ["fiber", "fork"]
TIER_S = ["sponsor", "donor", "token", "card", "link", "planet",
          "board", "cat", "ill", "hen", "cause", "use"]

def eth_addr(key):
    if hasattr(key, "secret"):
        s = key.secret
        s = s if isinstance(s, bytes) else s()
    elif isinstance(key, bytes):
        s = key
    else:
        s = bytes(key)
    pub = PublicKey.from_valid_secret(s).format(compressed=False)[1:]
    k = keccak.new(digest_bits=256); k.update(pub)
    return "0x" + k.hexdigest()[-40:]

def build_words(fp, pool_perm, remaining):
    w = [""] * 12
    for i, a in ANCHORS.items(): w[i] = a
    w[fp[0]] = UNPLACED[0]; w[fp[1]] = UNPLACED[1]
    for i, idx in enumerate(remaining): w[idx] = pool_perm[i]
    return " ".join(w)

def worker(wid, jobs, targets, shared):
    tested = 0; valid = 0; hits = []
    for fp, remaining in jobs:
        for pp in permutations(TIER_S, 7):
            m = build_words(fp, pp, remaining)
            tested += 1
            try:
                bip39.mnemonic_to_bytes(m)
            except ValueError:
                continue
            valid += 1
            root = bip32.HDKey.from_seed(bip39.mnemonic_to_seed(m))
            a = eth_addr(root.derive(PATH).key)
            if a in targets:
                hits.append((m, a))
        shared[wid] = tested
    return tested, valid, hits

def main():
    free = [i for i in range(12) if i not in ANCHORS]
    jobs = []
    for fp in permutations(free, 2):
        remaining = [i for i in free if i not in fp]
        jobs.append((fp, remaining))
    
    # WITNESS PROTOCOL: plant 2 known-valid candidates
    targets = {TARGET}
    witnesses = []
    for fp, remaining in jobs:
        for pp in permutations(TIER_S, 7):
            m = build_words(fp, pp, remaining)
            try:
                bip39.mnemonic_to_bytes(m)
            except ValueError:
                continue
            root = bip32.HDKey.from_seed(bip39.mnemonic_to_seed(m))
            witnesses.append((m, eth_addr(root.derive(PATH).key)))
            if len(witnesses) >= 2: break
        if len(witnesses) >= 2: break
    
    for m, a in witnesses:
        targets.add(a)
        print("[WITNESS] planted:", m)
    
    n = mp.cpu_count() or 4
    chunks = [jobs[i::n] for i in range(n)]
    mgr = mp.Manager(); shared = mgr.dict()
    
    import threading
    done_flag = threading.Event()
    def monitor():
        while not done_flag.is_set():
            try:
                tot = sum(shared.values())
            except Exception:
                tot = 0
            print(f"[PROGRESS] {tot/1e6:.1f}M / 287.4M lists", flush=True)
            time.sleep(60)
    threading.Thread(target=monitor, daemon=True).start()
    
    t0 = time.time()
    with mp.Pool(n) as pool:
        results = pool.starmap(worker, [(i, c, targets, shared) for i, c in enumerate(chunks)])
    done_flag.set()
    
    tested = sum(r[0] for r in results); valid = sum(r[1] for r in results)
    allhits = [h for r in results for h in h[2]]
    whits = [h for h in allhits if h[1] != TARGET]
    print(f"[DONE] tested={tested} valid={valid} t={time.time()-t0:.0f}s")
    
    if len(whits) < 2:
        print("[FAULT] witnesses not recovered -> NEGATIVE IS UNTRUSTED")
    
    for m, a in allhits:
        if a == TARGET:
            print("!!! HIT !!!", m, "-> SWEEP IMMEDIATELY (Rule #21)")
    
    if not any(a == TARGET for m, a in allhits):
        print("[RESULT] Tier-S negative (witnessed)" if len(whits) == 2 else "[RESULT] FAULT")

if __name__ == "__main__":
    main()
