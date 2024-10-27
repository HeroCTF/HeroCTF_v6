# State

### Category

Crypto

### Description

Could you decrypt the flag without the key ? Probably not.<br>
Could you decrypt the flag with the stack ? Maaaaaaaybe ...<br>
No the key isn't in the stack, what did you expect ?<br><br>
Format : **Hero{flag}**<br>
Author : **Alol**

### Files

- [state.zip](state.zip)

### Write Up

The binary reads the flag file, encrypts the flag with a 16 byte random key with RC4 and prints it to the screen. The key and flag are both stored on the heap (which we don't have) but the internal state of the RC4 algorithm isn't, it's stored on the stack.

The internal state of an RC4 algorithm is a 256 byte array of (randomly ordered) unique bytes, we can use the fact that this pattern has a very low probability of appearing to search for it in the stack. To optimise the search we can use a ["sliding window"](https://stackoverflow.com/questions/8269916/what-is-sliding-window-algorithm-examples) technique, illustrated below.

<p align="center">
  <img alt="Sliding window" src="https://miro.medium.com/v2/resize:fit:1400/0*eBgs1eCLHhc6vwU_.gif">
</p>

Once the state has been found we have to "rewind it" to the point where it was before the flag was encrypted. Then, all that's left is to decrypt and submit the flag!

```py
import subprocess
import sys
import re

CIPHERTEXT = bytes.fromhex(
    "ed8cad8dd3853655e490988aedab6e07332aafb1995fe529f6f0d89b82fe"
)


class RC4:
    def __init__(self, key: bytes) -> None:
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def PRGA(self) -> int:
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256

            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[(self.S[i] + self.S[j]) % 256]
            yield K

    def encrypt(self, plaintext: bytes) -> bytes:
        keystream = self.PRGA()
        return bytes(bytearray([c ^ next(keystream) for c in plaintext]))


def false_positive(b: list) -> bool:
    """
    Counts the number of times sequential items in a list go from increasing to
    decreasing (and vice-versa). Kind of like if the input list was sequential
    outputs of a polynomial and we were trying to find its degree.
    """

    x = 0
    for i in range(1, len(b)):
        if b[i - 1] > b[i]:
            x += 1
    return x in [0, 1, 254, 255]


def recover_plaintext(ct: bytes, output_state: list) -> None:
    """
    We know x (the length of the flag) but we don't know y. It's small so we can
    just bruteforce it.
    """

    for y in range(256):
        i, j = len(ct), y

        state = [*output_state]

        while i != 0:
            state[i], state[j] = state[j], state[i]
            j = (j - state[i]) % 256
            i = (i - 1) % 256

        if j != 0:
            continue

        rc4 = RC4(b"dummykey")
        rc4.S = [*state]
        flag = rc4.encrypt(CIPHERTEXT)

        if flag.isascii() and flag.startswith(b"Hero{") and flag.endswith(b"}"):
            print("Flag:", flag, (len(ct), y))


with open(sys.argv[1], "rb") as f:
    s = f.read()
    start = 0
    char_map = {}

    # The idea here is the same as if we were searching for the longest
    # non-repeating substring, the longest possible substring is 256 bytes
    # long since there are only 256 possible byte values.

    for end in range(len(s)):
        if s[end] in char_map:
            start = max(start, char_map[s[end]] + 1)
        char_map[s[end]] = end

        if end - start + 1 == 256 and not false_positive(s[start : end + 1]):
            state = list(s[start : end + 1])
            print(f"Key at {hex(start)}:", state)
            recover_plaintext(CIPHERTEXT, state)

"""
[alol@laptop State]$ python3 solve.py state/stack.bin 
 89%|█████████████████████████████████████████████████████████▋       | 120086/135168 [00:00<00:00, 1200657.90it/s]Key at 0x20ae0: [74, 254, 144, 135, 87, 143, 133, 55, 112, 137, 141, 11, 94, 12, 222, 161, 192, 234, 193, 78, 146, 64, 46, 109, 72, 106, 220, 237, 217, 35, 142, 149, 179, 107, 165, 37, 36, 48, 243, 189, 184, 4, 125, 103, 138, 96, 206, 38, 232, 20, 115, 180, 208, 80, 118, 129, 182, 210, 5, 66, 246, 150, 3, 14, 44, 8, 40, 207, 152, 81, 100, 24, 13, 39, 218, 108, 134, 174, 25, 110, 166, 0, 236, 69, 43, 10, 214, 15, 145, 226, 187, 132, 111, 73, 181, 61, 68, 86, 54, 19, 190, 136, 26, 253, 9, 197, 241, 71, 128, 147, 171, 60, 151, 117, 104, 17, 177, 188, 16, 240, 195, 88, 85, 33, 57, 32, 127, 139, 82, 213, 209, 205, 27, 158, 148, 160, 153, 120, 169, 183, 30, 31, 178, 62, 172, 229, 173, 102, 225, 168, 123, 76, 176, 199, 29, 47, 67, 23, 77, 22, 70, 251, 215, 155, 163, 156, 63, 249, 51, 167, 201, 130, 65, 84, 2, 228, 126, 122, 186, 98, 6, 250, 21, 58, 157, 52, 105, 119, 91, 83, 200, 93, 97, 235, 242, 170, 18, 185, 89, 211, 223, 1, 230, 221, 56, 53, 95, 247, 198, 248, 90, 140, 216, 191, 227, 233, 131, 175, 34, 162, 239, 154, 244, 245, 116, 219, 121, 202, 212, 45, 101, 238, 194, 224, 252, 92, 164, 231, 255, 203, 113, 114, 196, 28, 79, 7, 99, 75, 41, 159, 204, 42, 59, 50, 49, 124]
Flag: b'Hero{AESKeyFinder_but_for_RC4}' (30, 0)
100%|█████████████████████████████████████████████████████████████████| 135168/135168 [00:00<00:00, 1200542.28it/s]

"""
```

### Flag

- Hero{AESKeyFinder_but_for_RC4}
