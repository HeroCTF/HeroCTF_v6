# Halloween

### Category

Crypto

### Description

Boo! Do you believe in ghosts ? I sure don't.<br><br>
Host : **nc crypto.heroctf.fr 9001**<br>
Format : **Hero{flag}**<br>
Author : **Alol**

### Files

- [halloween.zip](halloween.zip)

### Write up

The challenge prints the encrypted flag before repeatedly encrypting user-submitted data. On the surface this is not vulnerable code, the key and nonce are generated properly meaning that the keystream should be 2\*\*68 bytes long before the counter wraps around and the keystream repeats. We need to dig deeper.

Looking into the source code we find this function that, supposedly, increments the counter.
```py
# https://github.com/drobotun/gostcrypto/blob/master/gostcrypto/gostcipher/gost_34_13_2015.py#L841C5-L841C8
    def _inc_ctr(self, ctr: bytearray) -> bytearray:
        internal = 0
        bit = bytearray(self.block_size)
        bit[self.block_size - 1] = 0x01
        for i in range(self.block_size):
            internal = ctr[i] + bit[i] + (internal << 8)
            ctr[i] = internal & 0xff
        return ctr
``` 

The screenshot below taken from one of the tickets I handled illustrates clearly what's wrong.

<p align="center">
  <img src="https://i.imgur.com/FfoNRKM.png">
</p>

The counter isn't incremented properly, effectively downgrading it from a 64 bit integer to a 8 bit integer. This, in turn, means that the keystream is now only 4096 bytes long. We can perform a chosen plaintext attack to recover the full keystream and decrypt the flag.

```py
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
```

### Flag

```Hero{5p00ky_5c4ry_fl4w3d_cryp70_1mpl3m3n74710ns_53nd_5h1v3r5_d0wn_y0ur_5p1n3}```