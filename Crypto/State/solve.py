from tqdm import trange
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

    for end in trange(len(s)):
        if s[end] in char_map:
            start = max(start, char_map[s[end]] + 1)
        char_map[s[end]] = end

        if end - start + 1 == 256 and not false_positive(s[start : end + 1]):
            state = list(s[start : end + 1])
            print(f"Key at {hex(start)}:", state)
            recover_plaintext(CIPHERTEXT, state)
