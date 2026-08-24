import os
import time
import multiprocessing as mp
from itertools import permutations, product

TARGET = "0x9c2f44efad0c1e852a09df9939e6daf061140caf"
PATH = "m/44'/60'/0'/0/0"
ANCHORS = {0: "dutch", 5: "fog", 11: "parrot"}
HINTS = ["will", "only", "like", "round"]
UNPLACED = ["fiber", "fork"]

def worker_task(worker_id, perms_chunk, shared_stats, hit_queue):
    # Imports binnenin de worker om Windows spawn-errors met C-extensions te voorkomen
    from embit import bip39, bip32
    from coincurve import PublicKey
    from Crypto.Hash import keccak

    def get_eth_addr(child_key):
        if isinstance(child_key, bytes): secret = child_key
        elif hasattr(child_key, "secret"):
            s = child_key.secret
            secret = s if isinstance(s, bytes) else s()
        else: secret = bytes(child_key)
        pub = PublicKey.from_valid_secret(secret)
        uncomp = pub.format(compressed=False)[1:]
        k = keccak.new(digest_bits=256)
        k.update(uncomp)
        return "0x" + k.hexdigest()[-40:]

    tested = 0
    valid = 0
    shared_stats[worker_id] = {"tested": 0, "valid": 0}

    try:
        for u_pos in perms_chunk:
            words = [""] * 12
            for idx, word in ANCHORS.items(): words[idx] = word
            words[u_pos[0]] = UNPLACED[0]
            words[u_pos[1]] = UNPLACED[1]
            remaining = [i for i in range(12) if words[i] == ""]

            for hint_combo in product(HINTS, repeat=7):
                final_words = words[:]
                for i, idx in enumerate(remaining):
                    final_words[idx] = hint_combo[i]
                mnemonic = " ".join(final_words)
                tested += 1
                try:
                    seed = bip39.mnemonic_to_seed(mnemonic)
                    valid += 1
                    root = bip32.HDKey.from_seed(seed)
                    child = root.derive(PATH)
                    addr = get_eth_addr(child.key)
                    if addr == TARGET:
                        hit_queue.put(mnemonic)
                        return
                except ValueError:
                    pass
                
                if tested % 2000 == 0:
                    shared_stats[worker_id] = {"tested": tested, "valid": valid}
        
        shared_stats[worker_id] = {"tested": tested, "valid": valid, "done": True}
    except Exception as e:
        shared_stats[worker_id] = {"error": str(e)}

def brain_orchestrator():
    print("="*70)
    print("SWARM ARCHITECTURE: BRAIN ORCHESTRATING WORKERS")
    print("="*70)
    
    free_indices = [i for i in range(12) if i not in ANCHORS]
    all_perms = list(permutations(free_indices, 2))
    
    num_workers = os.cpu_count() or 4
    total_combos = len(all_perms) * (4**7)
    
    print(f"[Brain] Analyzing search space: {total_combos:,} combos")
    print(f"[Brain] Spawning {num_workers} Worker Agents (CPU Cores)...")
    
    chunk_size = max(1, len(all_perms) // num_workers)
    chunks = [all_perms[i:i + chunk_size] for i in range(0, len(all_perms), chunk_size)]
    
    mgr = mp.Manager()
    shared_stats = mgr.dict()
    hit_queue = mgr.Queue()
    
    processes = []
    start_time = time.time()
    
    for i, chunk in enumerate(chunks):
        p = mp.Process(target=worker_task, args=(i, chunk, shared_stats, hit_queue))
        p.start()
        processes.append(p)
        
    active_workers = len(processes)
    last_print = time.time()
    
    while active_workers > 0:
        if not hit_queue.empty():
            mnemonic = hit_queue.get()
            print("\n" + "="*70)
            print("!!! HIT FOUND BY SWARM !!!")
            print(f"Mnemonic: {mnemonic}")
            print("="*70)
            for p in processes: p.terminate()
            return
            
        if time.time() - last_print >= 1.0:
            total_t = sum(s.get("tested", 0) for s in shared_stats.values() if isinstance(s, dict))
            total_v = sum(s.get("valid", 0) for s in shared_stats.values() if isinstance(s, dict))
            rate = total_t / max(time.time() - start_time, 0.1)
            eta_m = ((total_combos - total_t) / rate) / 60 if rate > 0 else 0
            print(f"\r[Brain] Tested: {total_t:,} | Valid: {total_v:,} | Rate: {rate:.0f}/s | ETA: {eta_m:.1f}m | Active: {active_workers}", end="", flush=True)
            last_print = time.time()
            
        alive = [p for p in processes if p.is_alive()]
        if len(alive) < active_workers:
            active_workers = len(alive)
        time.sleep(0.1)
        
    print("\n\n" + "="*70)
    print("[Brain] Swarm finished. No hit found.")
    print("="*70)

if __name__ == '__main__':
    brain_orchestrator()