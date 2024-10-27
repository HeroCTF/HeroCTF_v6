from flask import Flask, render_template, request, jsonify

import hashlib
import json
from os import getenv
from datetime import datetime


app = Flask(__name__)
FLAG = getenv("FLAG", "Hero{FAKE_FLAG}")

def compute_sha256(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode("utf-8"))
    return sha256_hash.hexdigest()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/prizes", methods=["POST"])
def claim_prizes():
    data = request.json
    date_str = data.get("date")
    received_signature = request.headers.get("X-Signature")

    json_data = json.dumps(data)
    expected_signature = compute_sha256(json_data)

    if not received_signature == expected_signature:
        return jsonify({"error": "Invalid signature"}), 400
    
    if not date_str:
        return jsonify({"error": "Date is missing"}), 400

    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        if date_obj.year >= 2100:
            return jsonify({"message": FLAG}), 200

        return jsonify({"error": "Please come back later..."}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
