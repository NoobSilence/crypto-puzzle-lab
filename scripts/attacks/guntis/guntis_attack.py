import hmac,hashlib,itertools
from embit import bip39
from coincurve import PrivateKey as CPriv
from Crypto.Hash import keccak

TARGET="0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF".lower()

def k256(d):
    h=keccak.new(digest_bits=256);h.update(d);return h.digest()

def cs_ok(words):
    try:WL=bip39.WORDLIST
    except AttributeError:
        import requests
        WL=requests.get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt",timeout=10).text.split()
    IDX={w:i for i,w in enumerate(WL)}
    if len(words)!=12:return False
    if not all(w in IDX for w in words):return False
    bits=0
    for w in words:bits=(bits<<11)|IDX[w]
    return (hashlib.sha256((bits>>4).to_bytes(16,"big")).digest()[0]>>4)==(bits&0xF)

def eth_addr(words,pp=""):
    seed=bip39.mnemonic_to_seed(" ".join(words),pp)
    I=hmac.new(b"Bitcoin seed",seed,hashlib.sha512).digest()
    kb,chain=I[:32],I[32:]
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    for idx in[0x80000000|44,0x80000000|60,0x80000000|0,0,0]:
        if idx&0x80000000:data=b"\x00"+kb+idx.to_bytes(4,"big")
        else:data=CPriv(kb).public_key.format(True)+idx.to_bytes(4,"big")
        I=hmac.new(chain,data,hashlib.sha512).digest()
        kb=((int.from_bytes(kb,"big")+int.from_bytes(I[:32],"big"))%n).to_bytes(32,"big")
        chain=I[32:]
    pub=CPriv(kb).public_key.format(False)
    return "0x"+k256(pub[1:])[12:].hex()

print("Certificering...")
assert eth_addr(["abandon"]*11+["about"])=="0x9858effd232b4033e47d90003d41ec34ecaeda94"
print("✓ GUNTIS gecertificeerd\n")

# Laad BIP39 woordenlijst
import requests
try:WL=bip39.WORDLIST
except AttributeError:
    WL=requests.get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt",timeout=10).text.split()
WSET=set(WL)

# Alternatieven voor niet-BIP39 woorden
VIDEO_VARIANTS=[
    ["fog","lake","parrot","goat","fork"],  # kern
    ["dark","night","black","dim"],  # dark alternatieven
    ["sing","song"],  # optioneel
]
POST_VARIANTS=[
    ["round","dutch","cattle","forest","wood","fiber"],  # kern
    ["hunter","hunt"],  # hunter alternatieven
    ["fresh","new"],  # fresh alternatieven
]

# Genereer alle video 6-combinaties
video_combos=[]
for v5 in [VIDEO_VARIANTS[0]+[d] for d in VIDEO_VARIANTS[1]]:  # 5 kern + 1 dark variant
    for extra in VIDEO_VARIANTS[2]:
        v6=v5+[extra]
        if all(w in WSET for w in v6):
            video_combos.append(v6)

# Genereer alle post 6-combinaties
post_combos=[]
for p6_base in POST_VARIANTS[0]:  # 6 kern woorden
    if all(w in WSET for w in p6_base):
        post_combos.append(p6_base)
# Test ook met hunter/fresh vervangen
for hunt in POST_VARIANTS[1]:
    for fresh in POST_VARIANTS[2]:
        p6=[w for w in POST_VARIANTS[0][:5]]+[hunt,fresh]
        if len(p6)==6 and all(w in WSET for w in p6):
            post_combos.append(p6)

print(f"Video combinaties: {len(video_combos)}")
print(f"Post combinaties: {len(post_combos)}")

# Passphrases
PASS=["","10","ETH","10ETH","guntis","mineshop","challenge","10 eth"]

hits=[];n=0
for vc in video_combos:
    for pc in post_combos:
        for seq in [vc+pc,pc+vc]:
            if cs_ok(seq):
                for pp in PASS:
                    n+=1
                    a=eth_addr(seq,pp)
                    if a==TARGET:
                        hits.append((seq,pp))
                        print(f"\n🎉🎉 HIT! SEED: {' '.join(seq)} PASS: '{pp}'\n")

print(f"\n{n} combinaties getest")
print("🏁 GUNTIS klaar." if not hits else "")
   