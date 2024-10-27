#!/usr/bin/env python3
import gostcrypto
import os

with open("flag.txt", "rb") as f:
    flag = f.read()

key, iv = os.urandom(32), os.urandom(8)
cipher = gostcrypto.gostcipher.new(
    "kuznechik", key, gostcrypto.gostcipher.MODE_CTR, init_vect=iv
)

print(f"It's almost Halloween, time to get sp00{cipher.encrypt(flag).hex()}00ky 👻!")

while True:
    print(cipher.encrypt(bytes.fromhex(input())).hex())
