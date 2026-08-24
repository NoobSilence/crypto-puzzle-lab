import urllib.request
import json
import time
import re

TARGET_WALLET = "0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF"
API_KEY = "YourApiKeyToken" 

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[ERROR] Fetch failed: {e}")
        return None

def decode_hex_to_ascii(hex_str):
    if not hex_str or hex_str == "0x":
        return ""
    try:
        bytes_str = bytes.fromhex(hex_str[2:])
        ascii_text = re.sub(r'[^ -~]+', '', bytes_str.decode('latin-1'))
        return ascii_text.strip()
    except:
        return ""

print("=" * 70)
print("AGENT 5: ON-CHAIN ARTIFACT & HEX DATA HUNTER")
print("=" * 70)

print("\n[PHASE 1] Fetching Token Transfers (ERC-20)...")
url_tok = f"https://api.etherscan.io/api?module=account&action=tokentx&address={TARGET_WALLET}&startblock=0&endblock=999999999&sort=asc&apikey={API_KEY}"
tok_data = fetch_json(url_tok)

if tok_data and tok_data.get("status") == "1":
    unique_tokens = {}
    for tx in tok_data["result"]:
        symbol = tx.get("tokenSymbol", "UNKNOWN")
        name = tx.get("tokenName", "UNKNOWN")
        contract = tx.get("contractAddress", "")
        
        if symbol not in unique_tokens:
            unique_tokens[symbol] = {"name": name, "contract": contract, "first_seen": tx.get("timeStamp")}
            
    print(f"\n🔍 FOUND {len(unique_tokens)} UNIQUE TOKENS IN WALLET:")
    for sym, info in unique_tokens.items():
        print(f"   - {sym} ({info['name']})")
        print(f"     Contract: {info['contract']}")
else:
    print("   [!] Token fetch failed or rate limited.")

print("\n[PHASE 1b] Fetching NFT Transfers (ERC-721/1155)...")
url_nft = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={TARGET_WALLET}&startblock=0&endblock=999999999&sort=asc&apikey={API_KEY}"
nft_data = fetch_json(url_nft)

if nft_data and nft_data.get("status") == "1":
    print(f"\n🖼️ FOUND {len(nft_data['result'])} NFT TRANSFERS:")
    for tx in nft_data["result"]:
        print(f"   - NFT: {tx.get('tokenName')} | ID: {tx.get('tokenID')}")
        print(f"     Contract: {tx.get('contractAddress')}")
else:
    print("   [!] NFT fetch failed.")

print("\n[PHASE 2] Decoding HEX Input Data of all transactions...")
url_tx = f"https://api.etherscan.io/api?module=account&action=txlist&address={TARGET_WALLET}&startblock=0&endblock=999999999&sort=asc&apikey={API_KEY}"
tx_data = fetch_json(url_tx)

if tx_data and tx_data.get("status") == "1":
    print(f"\n📜 SCANNING {len(tx_data['result'])} TRANSACTIONS FOR HIDDEN ASCII:")
    for tx in tx_data["result"]:
        hex_input = tx.get("input", "0x")
        decoded = decode_hex_to_ascii(hex_input)
        
        if decoded and len(decoded) > 2:
            print(f"\n   [TX HASH]: {tx['hash'][:15]}...")
            print(f"   [DECODED HIDDEN TEXT]: '{decoded}'")
else:
    print("   [!] TX list fetch failed.")

print("\n" + "=" * 70)
print("ARTIFACT HUNTER COMPLETE")
print("=" * 70)
