from Crypto.Util.number import long_to_bytes, bytes_to_long
from itertools import product
import hashlib
import string
import tqdm
import pwn

CHARSET = string.ascii_letters + string.digits + "_{}"

F = FiniteField(2**256 - 189)
R = PolynomialRing(F, "x")
H = lambda n: int(hashlib.sha256(n).hexdigest(), 16)

#r = pwn.process(["sage", "chall.sage"])
r = pwn.remote("crypto.heroctf.fr", int(9000))

points = eval(r.recvlineS())
points += [[0, H(b"Hero")]]

f = R.lagrange_polynomial(points)
print("Found polynomial", f)

coeffs = [*map(int, f.coefficients())]
flag = [b"____"] * len(coeffs)

for a, b, c, d in product(CHARSET, repeat=4):
    p = (a + b + c + d).encode()
    h = int(H(p))

    if h in coeffs:
        flag[coeffs.index(h)] = p
        print(b"".join(flag))
