// https://obfuscator.io/
function xorStrHex(a, b) {
    var res = '';
    for(var i=0;i<a.length;i++) {
        res += (parseInt(a[i], 16) ^ parseInt(b[i], 16)).toString(16);
    }
    return res;
}

function toHex(str) {
    var hex = '';
    for(var i=0;i<str.length;i++) {
        hex += ''+str.charCodeAt(i).toString(16);
    }
    return hex;
}

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