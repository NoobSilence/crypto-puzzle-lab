import hashlib,hmac
from embit import bip39,script,ec
from coincurve import PrivateKey as CPriv
def c_derive(words,first=84,pp=""):
    seed=bip39.mnemonic_to_seed(" ".join(words),pp)
    I=hmac.new(b"Bitcoin seed",seed,hashlib.sha512).digest()
    kb,chain=I[:32],I[32:]
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    for idx in[(0x80000000|first),(0x80000000|0),(0x80000000|0),0,0]:
        if idx&0x80000000:data=b"\x00"+kb+idx.to_bytes(4,"big")
        else:data=CPriv(kb).public_key.format(True)+idx.to_bytes(4,"big")
        I=hmac.new(chain,data,hashlib.sha512).digest()
        kb=((int.from_bytes(kb,"big")+int.from_bytes(I[:32],"big"))%n).to_bytes(32,"big")
        chain=I[32:]
    pub=ec.PublicKey.parse(CPriv(kb).public_key.format(True))
    return script.p2wpkh(pub).address() if first==84 else script.p2pkh(pub).address()
W=["abandon"]*11+["about"]
assert c_derive(W,84)=="bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"
assert c_derive(W,44)=="1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA"
print("LAPTOP GECERTIFICEERD")

