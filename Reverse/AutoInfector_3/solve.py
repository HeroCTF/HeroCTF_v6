#!/usr/bin/env python3
import requests


URL = "http://c2.capturetheflag.fr:4444/poll"

while True:
    resp = requests.get(
        URL,
        headers={"User-Agent": "WINDEV2407EVAL|||User|||192.168.1.28|||WIN_NT4|||9200"}
    )

    content = resp.content.decode()
    if "nothing" in content:
        print(".", end="", flush=True)
        continue

    print(content)
    break
