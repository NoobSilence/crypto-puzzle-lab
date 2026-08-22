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

# Laad BIP39 woordenlijst
import requests
try:WL=bip39.WORDLIST
except AttributeError:
    WL=requests.get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt",timeout=10).text.split()
WSET=set(WL)

# Alle BIP39 woorden uit de hints
VIDEO_BIP39=["fog","lake","parrot","goat","fork","sing","song"]  # 7 woorden
POST_BIP39=["round","dutch","cattle","forest","wood","fiber","hunter","fresh"]  # 8 woorden

print(f"Video BIP39 woorden ({len(VIDEO_BIP39)}): {VIDEO_BIP39}")
print(f"Post BIP39 woorden ({len(POST_BIP39)}): {POST_BIP39}\n")

# Genereer alle combinaties
video_combos=list(itertools.combinations(VIDEO_BIP39,6))
post_combos=list(itertools.combinations(POST_BIP39,6))

print(f"Video combinaties: {len(video_combos)}")
print(f"Post combinaties: {len(post_combos)}")
print(f"Totaal te testen: {len(video_combos) * len(post_combos) * 2}\n")

# Passphrases
PASS=["","10ETH","10eth","guntis","challenge","mineshop","10","eth"]

hits=[];n=0
checksum_ok=0
for vc in video_combos:
    for pc in post_combos:
        v6=list(vc)
        p6=list(pc)
        for seq in [v6+p6,p6+v6]:
            n+=1
            if cs_ok(seq,WL):
                checksum_ok+=1
                for pp in PASS:
                    a=eth_addr(seq,pp)
                    if a==TARGET:
                        hits.append((seq,pp))
                        print(f"\n🎉🎉 HIT! SEED: {' '.join(seq)} PASS: '{pp}'\n")

print(f"\n{n} combinaties getest")
print(f"{checksum_ok} hadden geldige checksum")
print("🏁 GUNTIS klaar." if not hits else "")