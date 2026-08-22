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

# VIDEO: exact 6 woorden in tekstvolgorde
VIDEO=["fog","lake","parrot","sing","song","goat"]

# POST: 7 woorden, kies 6 (laat 1 weg)
POST7=["round","dutch","cattle","forest","wood","fiber","fresh"]

print(f"Video (vast): {VIDEO}")
print(f"Post (7, kies 6): {POST7}\n")

PASS=["","10ETH","10eth","guntis","challenge","mineshop","10","eth","ETH","Guntis","parrot","goat","fog","dutch","10 eth","10ETHchallenge"]

hits=[];n=0
for skip in POST7:  # laat 1 post-woord weg
    p6=[w for w in POST7 if w!=skip]
    for seq in [VIDEO+p6,p6+VIDEO]:
        if cs_ok(seq,WL):
            for pp in PASS:
                n+=1
                a=eth_addr(seq,pp)
                if a==TARGET:
                    hits.append((seq,pp))
                    print(f"\n🎉🎉 HIT! SEED: {' '.join(seq)} PASS: '{pp}'\n")

print(f"{n} checksum-combinaties getest met passphrases")
print("🏁 GUNTIS klaar." if not hits else "")