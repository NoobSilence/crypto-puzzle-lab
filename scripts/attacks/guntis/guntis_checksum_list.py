import hmac,hashlib,itertools
from embit import bip39
from coincurve import PrivateKey as CPriv
from Crypto.Hash import keccak

TARGET="0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF".lower()

def k256(d):
    h=keccak.new(digest_bits=256);h.update(d);return h.digest()

def cs_ok(words,WL):
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

import requests
try:WL=bip39.WORDLIST
except AttributeError:
    WL=requests.get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt",timeout=10).text.split()

VIDEO_BIP39=["fog","lake","parrot","goat","fork","sing","song"]
POST_BIP39=["round","dutch","cattle","forest","wood","fiber","hunter","fresh"]

video_combos=list(itertools.combinations(VIDEO_BIP39,6))
post_combos=list(itertools.combinations(POST_BIP39,6))

checksum_combos=[]
for vc in video_combos:
    for pc in post_combos:
        v6=list(vc)
        p6=list(pc)
        for seq in [v6+p6,p6+v6]:
            if cs_ok(seq,WL):
                checksum_combos.append(seq)

print(f"\n{len(checksum_combos)} combinaties met checksum:\n")
for i,combo in enumerate(checksum_combos,1):
    print(f"{i}. {' '.join(combo)}")
    
# Test deze met meer passphrases
PASS=["","10ETH","10eth","guntis","challenge","mineshop","10","eth","ETH","Guntis","mineshop.eu","0x9C2F","9c2f","10ethchallenge","parrot","goat","dutch","fog"]

print(f"\n\nTesten met {len(PASS)} passphrases...\n")
hits=[]
for combo in checksum_combos:
    for pp in PASS:
        a=eth_addr(combo,pp)
        if a==TARGET:
            hits.append((combo,pp))
            print(f"🎉🎉 HIT! SEED: {' '.join(combo)} PASS: '{pp}'")

if not hits:
    print("Geen hit gevonden met deze passphrases")
    
print("\n🏁 Klaar")