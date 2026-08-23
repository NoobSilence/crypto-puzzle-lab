import json
import shutil
from pathlib import Path

base_dir = Path(__file__).parent.parent
bnb_path = base_dir / "knowledge_base" / "bnb_02btc.json"
guntis_path = base_dir / "knowledge_base" / "guntis_10eth.json"

def load_json(path):
    if not path.exists(): 
        print(f"WARNING: {path} not found")
        return {}
    with open(path, 'r', encoding='utf-8') as f: 
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved cleaned data to {path}")

print("=" * 50)
print("KNOWLEDGE BASE CLEANUP")
print("=" * 50)

# Clean BNB
print("\n[1] Cleaning bnb_02btc.json...")
bnb_data = load_json(bnb_path)
if bnb_data:
    keys_to_remove = [
        "mission_1b_clock_analysis", 
        "clock_verification", 
        "vision_voting_3agents", 
        "dial_cipher_verification", 
        "cipher_decoding_attempts", 
        "cipher_bip39_words", 
        "whitepaper_quote_verification"
    ]
    removed_count = 0
    for key in keys_to_remove:
        if key in bnb_data:
            del bnb_data[key]
            removed_count += 1
            print(f"  Removed: {key}")
    
    print(f"  Total keys removed: {removed_count}")
    
    # Make backup
    backup = bnb_path.with_suffix(".json.backup")
    if not backup.exists():
        shutil.copy(bnb_path, backup)
        print("  Backup created.")
    
    save_json(bnb_path, bnb_data)
else:
    print("  No data to clean (file empty or missing).")

# Clean Guntis
print("\n[2] Checking guntis_10eth.json...")
guntis_data = load_json(guntis_path)
if guntis_data:
    if "confirmed_positions" not in guntis_data:
        guntis_data["confirmed_positions"] = {"1": "dutch", "5": "fog", "12": "parrot"}
        print("  Added confirmed_positions.")
    
    if "unplaced" not in guntis_data:
        guntis_data["unplaced"] = ["fiber", "fork"]
        print("  Added unplaced words.")
        
    save_json(guntis_path, guntis_data)
    print("  Guntis data verified/saved.")
else:
    print("  WARNING: Guntis JSON not found.")

print("\nDONE")