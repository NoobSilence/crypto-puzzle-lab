import requests
import time

RPC_PROVIDERS = [
    "https://ethereum.publicnode.com",
    "https://eth.llamarpc.com",
    "https://rpc.ankr.com/eth",
    "https://eth-mainnet.public.blastapi.io",
    "https://1rpc.io/eth",
    "https://cloudflare-eth.com",
]

TARGETS = [
    ("PUZZLE_WALLET", "0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF"),
    ("DRAIN_DEST_1", "0xf755aaAce22fCFDCd4E300A3f26249000D95F1b2"),
    ("DRAIN_DEST_2", "0xa6Dc2F247ea9b9f48c434ECC5071AC7Ebb16c175"),
    ("DRAIN_DEST_3", "0xE708D1496EE95435eA50f3E4bC79c28A5f8Fe859"),
    ("DRAIN_DEST_4", "0xaAd9a1c75946D3dB263141659A6111B6De1F57c6"),
]

def try_all_rpc_providers(method, params):
    for rpc_url in RPC_PROVIDERS:
        payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            r = requests.post(rpc_url, json=payload, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                if "result" in data:
                    return data["result"], rpc_url
                elif "error" in data:
                    print(f"   [{rpc_url.split('/')[2]}] Error: {data['error']}")
            else:
                print(f"   [{rpc_url.split('/')[2]}] HTTP {r.status_code}")
        except Exception as e:
            print(f"   [{rpc_url.split('/')[2]}] Exception: {str(e)[:50]}")
        time.sleep(0.5)
    return None, None

def hex_to_eth(h):
    if h and h.startswith("0x"):
        return int(h, 16) / 10**18
    return 0

def hex_to_int(h):
    if h and h.startswith("0x"):
        return int(h, 16)
    return 0

print("=" * 70)
print("ON-CHAIN FORENSICS [MODE: PURE ZERO-DEP]")
print("=" * 70)

for label, addr in TARGETS:
    print(f"\n{'='*70}")
    print(f"[ TARGET: {label} ]")
    print(f"Address: {addr}")
    print(f"{'='*70}")
    
    print("\n🔍 Trying RPC providers for balance...")
    bal_hex, provider = try_all_rpc_providers("eth_getBalance", [addr, "latest"])
    
    if bal_hex:
        eth = hex_to_eth(bal_hex)
        print(f"✅ BALANCE: {eth:.8f} ETH (via {provider.split('/')[2]})")
        
        print("\n🔍 Getting nonce...")
        nonce_hex, _ = try_all_rpc_providers("eth_getTransactionCount", [addr, "latest"])
        if nonce_hex:
            nonce = hex_to_int(nonce_hex)
            activity = "🔥 HOT WALLET" if nonce > 50 else "🧊 COLD STORAGE" if nonce < 10 else "📊 MEDIUM ACTIVE"
            print(f"✅ NONCE: {nonce} transactions ({activity})")
        
        print("\n🔍 Checking if smart contract...")
        code_hex, _ = try_all_rpc_providers("eth_getCode", [addr, "latest"])
        if code_hex == "0x":
            print(f"✅ TYPE: EOA (Regular Wallet)")
        elif code_hex and code_hex.startswith("0x") and len(code_hex) > 2:
            print(f"⚠️ TYPE: SMART CONTRACT")
    else:
        print("\n❌ All RPC providers failed")
    
    print()
    time.sleep(2)

print("\n" + "=" * 70)
print("FORENSIC ANALYSIS COMPLETE")
print("=" * 70)
