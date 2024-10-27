from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from collections import OrderedDict
from tqdm import tqdm, trange
import sys
import os

pt_banner = b"I don't trust governments, thankfully I've found smart a way to keep my data secure."
ct_banner = b"\xd5\xae\x14\x9de\x86\x15\x88\xe0\xdc\xc7\x88{\xcfy\x81\x91\xbaH\xb6\x06\x02\xbey_0\xa5\x8a\xf6\x8b?\x9c\xc9\x92\xac\xdeb=@\x9bI\xeeY\xa0\x8d/o\xfa%)\xfb\xa2j\xd9N\xf7\xfd\xf6\xc2\x0b\xc3\xd2\xfc\te\x99\x9aIG\x01_\xb3\xf4\x0fG\xfb\x9f\xab\\\xe0\xcc\x92\xf5\xaf\xa2\xe6\xb0h\x7f}\x92O\xa6\x04\x92\x88"
enc_flag = b"\xaf\xe0\xb8h=_\xb0\xfbJ0\xe6l\x8c\xf2\xad\x14\xee\xccw\xe9\xff\xaa\xb2\xe9c\xa4\xa0\x95\x81\xb8\x03\x93\x7fg\x00v\xde\xba\xfe\xb92\x04\xed\xc4\xc7\x08\x8c\x96C\x97\x07\x1b\xe8~':\x91\x08\xcf\x9e\x81\x0b\x9b\x15"
k0 = b'C\xb0\xc0f\xf3\xa8\n\xff\x8e\x96g\x03"'
k1 = b"Q\x95\x8b@\xfbf\xba_\x9e\x84\xba\x1a7"


def encrypt_AES(data: bytes, key: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def decrypt_SM4(data: bytes, key: bytes) -> bytes:
    cipher = Cipher(algorithms.SM4(key), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def decrypt_AES(data: bytes, key: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


ENC = OrderedDict()
DEC = OrderedDict()

print("Calculating dicts...")
for a in trange(256):
    for b in range(256):
        for c in range(256):
            part = bytes(bytearray([a, b, c]))
            ENC[encrypt_AES(pt_banner[:16], part + k0)] = part
            DEC[decrypt_SM4(ct_banner[:16], part + k1)] = part


print("Dicts done at last", len(ENC))
print("Recovering secret key...")

for part in tqdm(DEC):
    if part in ENC:
        print("Ding! Ding! Ding!")
        k0, k1 = ENC[part] + k0, DEC[part] + k1
        break
else:
    print("Couldn't MITM")
    sys.exit(1)

print(decrypt_AES(decrypt_SM4(enc_flag, k1), k0))
