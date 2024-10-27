# Interpolation

### Category

Crypto

### Description

Has missing data really ever stopped anyone ?<br><br>
Host : **nc crypto.heroctf.fr 9000**<br>
Format : **Hero{flag}**<br>
Author : **Alol**

### Files

- [interpolation.zip](interpolation.zip)

### Write up

The challenge generates coefficients for a polynomial of degree 23 by splitting the flag into chunks of four bytes and hashing them. The challenge then gives the user 23 random points. The naive approach would be to use Lagrange interpolation to recover the original polynomial given these points but that requires **n+1** points, here we only have **n**.
Thankfully, we know that from the way the polynomial was generated, the coefficient of x_{0} is the SHA256 hash of the bytes b'Hero'. This means that `f(0) = H(b'Hero')`, thus we know the **n+1**-th point needed for Lagrange interpolation.
Once the polynomial is retrieved, we can bruteforce the flag chunk by chunk.

```py
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

"""
Found polynomial 91356407137791927144958613770622174607926961061379368852376771002781151613901*x^23 + 58688474918974956495962699109478986243962548972465028067725936901754910032197*x^22 + 71177914266346294875020009514904614231152252028035180341047573071890295627281*x^21 + 9286536496641678624961072298289256247776902880262474453231051084428770229931*x^20 + 48478433129988933656911497337570454952912987663301800112434018755270886790086*x^19 + 105484582062398143020926667398250530293520625898492636870365251172877956081489*x^18 + 91842050171741174464568525719602040646922469791657773826919079592778110767648*x^17 + 43594818259201189283635356607462328520192502107771693650896092861477784342431*x^16 + 66681440692524165569992671994842901187406728987456386756946647843877275534778*x^15 + 7092396080272228853132842491037895182885372693653833621714864119915575351959*x^14 + 115533839068795212658451397535765278473898133068309149603041276877934373391258*x^13 + 32403908412257070302225532346590438994349383666861558172214850130936584778364*x^12 + 15596341609452054024790211046165535925702287406391095849367220616094959319247*x^11 + 98676420105970876355731743378079563095438931888109560800924537433679751968410*x^10 + 4587316730151077745530345853110346550953429707066041958662730783235705675823*x^9 + 4244268215373067710299345981438357655695365045434952475766578691548900068884*x^8 + 78645989056858155953548111309497253790838184388240819797824701948971210482613*x^7 + 10009681240064642703458239750230614173777134131788316383198404412696086812123*x^6 + 16605552275238206773988750913306730384585706182539455749829662274657349564685*x^5 + 42828444749577646348433379946210116268681295505955485156998041972023283883825*x^4 + 78252810134582863205690878209501272813895928209727562041762503202357420752872*x^3 + 54922548012150305957596790093591596584466927559339793497872781061995644787934*x^2 + 37382279584575671665412736907293996338695993273870192478675632069138612724862*x + 51862623363251592162508517414206794722184767070638202339849823866691337237984
b'________________________________________________________h0_c____________________________________'
b'________________________________l3_1____________________h0_c____________________________________'
b'________________________________l3_1____________________h0_c________________________mpl3________'
b'________________________________l3_1n_th________________h0_c________________________mpl3________'
b'________________________________l3_1n_th________________h0_c________p0l4____________mpl3________'
b'____________________________p30pl3_1n_th________________h0_c________p0l4____________mpl3________'
b'____________________________p30pl3_1n_th________________h0_c________p0l4____r0m_____mpl3________'
b'____________r3_t____________p30pl3_1n_th________________h0_c________p0l4____r0m_____mpl3________'
b'________r3_4r3_t____________p30pl3_1n_th________________h0_c________p0l4____r0m_____mpl3________'
b'________r3_4r3_t____________p30pl3_1n_th________________h0_c________p0l4____r0m_____mpl3t3_d____'
b'________r3_4r3_t____________p30pl3_1n_th________________h0_c________p0l4t3_fr0m_____mpl3t3_d____'
b'________r3_4r3_tw0_t________p30pl3_1n_th________________h0_c________p0l4t3_fr0m_____mpl3t3_d____'
b'________r3_4r3_tw0_t________p30pl3_1n_th________________h0_c____xtr4p0l4t3_fr0m_____mpl3t3_d____'
b'________r3_4r3_tw0_typ35____p30pl3_1n_th________________h0_c____xtr4p0l4t3_fr0m_____mpl3t3_d____'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th________________h0_c____xtr4p0l4t3_fr0m_____mpl3t3_d____'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th____0rld________h0_c____xtr4p0l4t3_fr0m_____mpl3t3_d____'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th____0rld________h0_c____xtr4p0l4t3_fr0m_1nc0mpl3t3_d____'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th15_w0rld________h0_c____xtr4p0l4t3_fr0m_1nc0mpl3t3_d____'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th15_w0rld________h0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d____'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th15_w0rld________h0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d474}'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th15_w0rld____53_wh0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d474}'
b'Hero____r3_4r3_tw0_typ35____p30pl3_1n_th15_w0rld_th053_wh0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d474}'
b'Hero____r3_4r3_tw0_typ35_0f_p30pl3_1n_th15_w0rld_th053_wh0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d474}'
b'Hero{th3r3_4r3_tw0_typ35_0f_p30pl3_1n_th15_w0rld_th053_wh0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d474}'
"""
```

### Flag

```Hero{th3r3_4r3_tw0_typ35_0f_p30pl3_1n_th15_w0rld_th053_wh0_c4n_3xtr4p0l4t3_fr0m_1nc0mpl3t3_d474}```