import requests
import json
import time
import re

RPC_URL = "https://ethereum.publicnode.com"

KNOWN_TX_HASHES = [
    "0xa0c970e0eacc199d3d8a617af84182861b886958fd4416399e9a7191f9dcfb70",
    "0xcf21ccdc94b490435909056531d165ad26eb78b8a2c7ad585376cc5febca0d1a",
    "0xd5fa39886433eed6bb2d18f3670ef881a9c7437768070ec3fc1749e5e89f8d7d",
    "0x751a87f5a2434a8a359e806fa446cf9873956a73e8c13e2de947fe0cd586c368",
    "0x16e05bf1d527b82e1a08b100c7255d9512ac2f989a05a6aec43112fb3bb34adb",
    "0x459acd3020f1b6ba8b3123a44aa62df802c31641ad5424ecb3a34b2db0482c2b",
    "0xd53379648d1eadcd779d4546dd877bce6c0ce976777ebe6feaa372df3b9d841e",
    "0x5ecca9595fa278b7cc348ceecd6bd784be3c13540ece7be9bde4cd611cd243de",
    "0xe5e71ab1a3c08c3936926c8b64bff40d4c5db41f228057a1dabab56eb258553c",
    "0x3131dd70cd075e62d2d790e920f2049b7bb25d2640c8ecf534257aed01aa3134",
    "0xf2debb3bcfd55e1af49593c5ee2e4e88c9f9f48ea6176618361d98b0a6617a7e",
    "0xe84fa359e4a901ed3555faf749c27710101ab124bc4395cbbeffe077d953f816",
]

def rpc_call(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.post(RPC_URL, json=payload, headers=headers, timeout=15)
        data = response.json()
        if "result" in data:
            return data["result"]
        elif "error" in data:
            print(f"   [RPC ERROR] {data['error']}")
        return None
    except Exception as e:
        print(f"   [REQUEST ERROR] {e}")
        return None

def decode_hex_to_ascii(hex_str):
    if not hex_str or hex_str == "0x":
        return "", hex_str
    try:
        bytes_str = bytes.fromhex(hex_str[2:])
        try:
            text = bytes_str.decode('utf-8', errors='ignore')
        except:
            text = bytes_str.decode('latin-1', errors='ignore')
        ascii_text = re.sub(r'[^ -~]+', '', text)
        return ascii_text.strip(), hex_str
    except Exception as e:
        return f"[DECODE ERROR: {e}]", hex_str

def check_bip39_words(text):
    bip39_sample = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb",
        "abstract", "absurd", "abuse", "access", "accident", "account",
        "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
        "action", "actor", "actress", "actual", "adapt", "add", "addict",
        "address", "adjust", "admit", "adult", "advance", "advice", "aerobic",
        "affair", "afford", "afraid", "again", "age", "agent", "agree",
        "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
        "alcohol", "alert", "alien", "all", "alley", "allow", "almost",
        "alone", "alpha", "already", "also", "alter", "always", "amateur",
        "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient",
        "anger", "angle", "angry", "animal", "ankle", "announce", "annual",
        "another", "answer", "antenna", "antique", "anxiety", "any", "apart",
        "apology", "appear", "apple", "approve", "april", "arch", "arctic",
        "area", "arena", "argue", "arm", "armed", "armor", "army",
        "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
        "artist", "artwork", "ask", "aspect", "assault", "asset", "assist",
        "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude",
        "attract", "auction", "audit", "august", "aunt", "author", "auto",
        "autumn", "average", "avocado", "avoid", "awake", "aware", "away",
        "awesome", "awful", "awkward", "axis"
    ]
    text_lower = text.lower()
    found = []
    for word in bip39_sample:
        if word in text_lower:
            found.append(word)
    return found

print("=" * 70)
print("AGENT 7: PURE RPC HEX DECODER")
print("Analyzing transaction input data for hidden messages")
print("=" * 70)

print(f"\n[INFO] Using RPC endpoint: {RPC_URL}")
print(f"[INFO] Analyzing {len(KNOWN_TX_HASHES)} known transactions\n")

results = []

for i, tx_hash in enumerate(KNOWN_TX_HASHES, 1):
    print(f"\n[TX {i}/{len(KNOWN_TX_HASHES)}] {tx_hash[:20]}...")
    
    tx_data = rpc_call("eth_getTransactionByHash", [tx_hash])
    
    if tx_data:
        input_hex = tx_data.get("input", "0x")
        from_addr = tx_data.get("from", "unknown")
        to_addr = tx_data.get("to", "contract creation")
        value_hex = tx_data.get("value", "0x0")
        value_eth = int(value_hex, 16) / 10**18 if value_hex != "0x0" else 0
        
        print(f"   From: {from_addr[:15]}...")
        print(f"   To:   {to_addr[:15] if to_addr else 'contract'}...")
        print(f"   Value: {value_eth:.6f} ETH")
        
        decoded_ascii, raw_hex = decode_hex_to_ascii(input_hex)
        
        if decoded_ascii and decoded_ascii not in ["", "[DECODE ERROR:"]:
            print(f"   📜 DECODED INPUT DATA:")
            print(f"      ASCII: '{decoded_ascii}'")
            
            bip39_found = check_bip39_words(decoded_ascii)
            if bip39_found:
                print(f"   🎯 BIP39 WORDS FOUND: {', '.join(bip39_found)}")
            
            results.append({
                "hash": tx_hash,
                "decoded": decoded_ascii,
                "bip39_words": bip39_found,
                "value": value_eth
            })
        else:
            if input_hex != "0x":
                print(f"   📜 RAW HEX (first 100 chars): {input_hex[:100]}...")
                results.append({
                    "hash": tx_hash,
                    "decoded": f"[HEX ONLY: {len(input_hex)} chars]",
                    "bip39_words": [],
                    "value": value_eth
                })
            else:
                print(f"   ℹ️  No input data (simple ETH transfer)")
    else:
        print(f"   ❌ Failed to fetch transaction data")
    
    time.sleep(0.5)

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

print(f"\n[SUMMARY]")
print(f"Total transactions analyzed: {len(KNOWN_TX_HASHES)}")
print(f"Transactions with input data: {len(results)}")

all_bip39 = []
for r in results:
    all_bip39.extend(r.get("bip39_words", []))

if all_bip39:
    print(f"\n🎯 BIP39 WORDS FOUND IN TRANSACTION DATA:")
    for word in set(all_bip39):
        print(f"   - {word}")
else:
    print(f"\nℹ️  No BIP39 words found in decoded input data")

print("\n[DETAILED RESULTS]")
for r in results:
    if r["decoded"] and r["decoded"] not in ["", "[HEX ONLY]"]:
        print(f"\nHash: {r['hash'][:20]}...")
        print(f"Value: {r['value']:.6f} ETH")
        print(f"Decoded: {r['decoded']}")
        if r["bip39_words"]:
            print(f"BIP39: {', '.join(r['bip39_words'])}")

print("\n" + "=" * 70)
print("HEX DECODER COMPLETE")
print("=" * 70)
