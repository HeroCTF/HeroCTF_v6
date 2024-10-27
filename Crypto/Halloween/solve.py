from pwn import *

BS = 16

# io = process(["python3", "chall.py"])
io = remote("crypto.heroctf.fr", 9001)

io.recvuntil(b"It's almost Halloween, time to get sp00")
flag = bytes.fromhex(io.recvuntil(b"00ky")[:-4].decode())
io.recvline()

io.sendline(b"00" * BS * 256)
keystream = bytes.fromhex(io.recvlineS())

print(xor(flag, keystream[-(1 + len(flag) // BS) * BS :])[: len(flag)])
