# AutoInfector 1/3

### Category

Reverse

### Description

Upon exploring shadowy online forums, you stumbled upon an article detailing a freshly emerged malware reseller. Your mission, spread across three challenges, is to download and analyze the multi-stage malware. To claim the first flag, find a method to download a beta version of this malware.

Format : Hero{flag}<br>
Author : xanhacks

### Write Up

After some javascript deobfusaction, the interesting code will look like this:

```js
document.getElementById("download-malware").onclick = function() {
    const title = document.title.split(" - ")[0];
    const hashTitle = hex_md5(title);
    const value = prompt("Enter the password to download the malware:");
    if (!value) {return;}
    const hashValue = hex_md5(value);
    const got = xorStrHex(hashTitle, hashValue);
    const expected = "11dfc83092be6f72c7e9e000e1de2960";
    if (got === expected) {
        alert(`You can validate the challenge with the following flag: Hero{${value}}`);
        window.location.href = `/${value}.exe`;
    } else {
        alert("Wrong password!");
    }
}
```

To deobfuscate the JS code, you can use your Browser's console and [https://lelinhtinh.github.io/de4js/](https://lelinhtinh.github.io/de4js/).

What we know:

- `title = 'AutoInfector';`
- `11dfc83092be6f72c7e9e000e1de2960 == hex_md5('AutoInfector') ^ hex_md5(input)`

What we want to find:

- `hex_md5(input) == 11dfc83092be6f72c7e9e000e1de2960 ^ hex_md5('AutoInfector')`
- `hex_md5(input) == 11dfc83092be6f72c7e9e000e1de2960 ^ e3df2713dfaefd4badf9b892ba54245f`
- `hex_md5(input) == f200ef234d1092396a1058925b8a0d3f`

We can use [https://crackstation.net/](https://crackstation.net/) to crack our MD5 hash and obtain the input `infectedmushroom`.

### Flag

Hero{infectedmushroom}