#!/usr/bin/env python3
import os
import random
from flask import Flask, request, send_file


app = Flask(__name__)
splitter = "|||"


@app.route('/stage2', methods=['POST'])
def stage2():
    user_agent = request.headers.get('User-Agent')
    if user_agent != "AutoInfector V1.0":
        return "Invalid User-Agent", 403

    _language = request.form.get('language')

    # Portuguese / Brazil
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN
    if _language != "00000416": 
        return "Invalid language", 403

    file_path = "/app/stage2.au3"
    return send_file(file_path, as_attachment=True)


def check_fingerprint(user_agent) -> tuple[bool, str]:
    # i.e. WINDEV2407EVAL|||User|||192.168.1.27|||WIN_11|||X64|||22621
    # i.e. WINDEV2407EVAL|||User|||192.168.1.28|||WIN_NT4|||9200
    user_agent = request.headers.get('User-Agent')
    if user_agent.count(splitter) != 4:
        return False, "Invalid User-Agent"

    _computer_name, _username, _ipaddress, _version, _build = user_agent.split(splitter)
    if not _computer_name:
        return False, "Invalid computer name"
    
    if not _username:
        return False, "Invalid username"

    if "." not in _ipaddress:
        return False, "Invalid IP Address"

    if "WIN" not in _version.upper():
        return False, "Invalid version"
    
    if not _build.isdigit():
        return False, "Invalid build"
    
    return True, ""


@app.route('/poll', methods=['GET'])
def poll():
    success, message = check_fingerprint(request.headers.get('User-Agent'))
    if not success:
        return message, 403

    responses = ["plugin" + splitter + "; " + os.getenv("FLAG_3")]
    for _ in range(30):
        responses.append("nothing" + splitter)

    return random.choice(responses), 200

@app.route('/send', methods=['POST'])
def send():
    success, message = check_fingerprint(request.headers.get('User-Agent'))
    if not success:
        return message, 403
    
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
