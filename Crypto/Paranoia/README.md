# Paranoia

### Category

Crypto

### Description

I always feel that somebody's watching me<br>
And I have *found a way to keep my* privacy (oh, oh)<br><br>
Format : **Hero{flag}**<br>
Author : **Alol**

### Files

- [paranoia.zip](paranoia.zip)

### Write up

At a glance, it seems that the only way to recover the flag is to bruteforce the missing key parts, which would take longer than the duration of the CTF without a significant cost investment.
The trick is to notice that the encryption function can be divided into the AES part and the SM4 part. They could be individually bruteforced because they use 24 bit keys but since they're chained together it's as if the keys combined into a 48 bit key.

<p align="center">
  <img alt="Naive bruteforce" src="https://miro.medium.com/v2/resize:fit:640/format:webp/1*RUawxLm3pWNrDerL1uepVA.gif">
</p>

The Meet in the Middle algorithm is perfect for this use case. [This video](https://www.youtube.com/watch?v=wL3uWO-KLUE) explains the algorithm nicely. Instead of going from the plaintext to the ciphertext we go from both `plaintext` and `ciphertext` to an intermediate ciphertext. We don't know what this intermediate ciphertext will be, only that it will be the same for `ENC(plaintext)` and `DEC(ciphertext)`. We can store `ENC(plaintext)` and `DEC(ciphertext)` for all possible keys in separate dictionaries, the intermediate ciphertext will be the intersection of these two dictionnaries. Doing so cuts the number of calculations from 2\*\*48 to 2\*\*25 (2\*\*24 keys for encryption + 2\*\*24 keys for decryption) but incurs a memory tradeoff (~608MB ideally but closer to 2GB in practice).

<p align="center">
  <img alt="Meet in the Middle" src="https://miro.medium.com/v2/resize:fit:640/format:webp/1*UMx_YWNvX2XN-GAlFMphZQ.gif">
</p>

To make the key recovery faster multiple options are available. Using the `multiprocessing` module (*not `threading`*, that's [bad](https://realpython.com/python-gil/)), using a different python interpreter like `pypy`, rewriting everything in Rust or abusing your university cluster to bruteforce.

```py
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

print("Starting meet in the middle")
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
    print("Couldn't MITM :(")
    sys.exit(1)

print(decrypt_AES(decrypt_SM4(enc_flag, k1), k0))

"""
[alol@laptop Paranoia]$ python3 solve_paranoia.py 
Calculating dicts...
100%|████████████████████████████████████████████████████████████████████████████| 256/256 [22:35<00:00,  5.29s/it]
Dicts done at last 16777216
Recovering secret key...
 58%|████████████████████████████████████▎                          | 9676938/16777216 [00:11<00:08, 824829.22it/s]Ding! Ding! Ding!
 58%|████████████████████████████████████▌                          | 9751442/16777216 [00:11<00:08, 827383.96it/s]
b'Hero{p4r4n014_p4r4n014_3v3ryb0dy_5_c0m1n6_70_637_m3!}\n\n\n\n\n\n\n\n\n\n\n'
"""
```

### Flag

```Hero{p4r4n014_p4r4n014_3v3ryb0dy_5_c0m1n6_70_637_m3!}```