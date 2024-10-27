from cryptography.hazmat.primitives.ciphers.algorithms import AES, SM4
from cryptography.hazmat.primitives.ciphers import Cipher, modes
import os


class Paranoia:
    def __init__(self, keys):
        self.keys = keys

    def __pad(self, data: bytes, bs: int) -> bytes:
        return data + (chr(bs - len(data) % bs) * (bs - len(data) % bs)).encode()

    def __encrypt(self, algorithm, data: bytes, key: bytes):
        cipher = Cipher(algorithm(key), modes.ECB())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def encrypt(self, data: bytes):
        """
        🇨🇳 encryption to protect against the 🇺🇸 backdoor and
        🇺🇸 encryption to protect against the 🇨🇳 backdoor

        I'm a genius !
        """

        data = self.__pad(data, 16)
        data = self.__encrypt(AES, data, self.keys[0])
        data = self.__encrypt(SM4, data, self.keys[1])
        return data


with open("flag.txt", "rb") as f:
    flag = f.read()

keys = [os.urandom(16) for _ in range(2)]
paranoia = Paranoia(keys)

banner = b"I don't trust governments, thankfully I've found smart a way to keep my data secure."

print("pt_banner =", banner)
print("ct_banner =", paranoia.encrypt(banner))
print("enc_flag  =", paranoia.encrypt(flag))

# To comply with cryptography export regulations,
# 6 bytes = 2**48 bits, should be bruteforce-proof anyway
for n, k in enumerate(keys):
    print(f"k{n} = {k[3:]}")
