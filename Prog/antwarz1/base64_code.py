import base64
import sys

b64_encoded = base64.b64encode(open(sys.argv[1]).read().encode()).decode()
lines = []
for i in range(0, len(b64_encoded), 1024):
    if i + 1024 < len(b64_encoded):
        lines.append(b64_encoded[i:i+1024])
    else:
        lines.append(b64_encoded[i:])

print("\n".join(lines))
print('EOF')