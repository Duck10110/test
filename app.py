from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fingerprint", methods=["POST"])
def fingerprint():
    data = request.get_json(silent=True) or {}

    log = {
        "time": datetime.utcnow().isoformat(),
        "ip": request.headers.get("x-forwarded-for", request.remote_addr),
        "ua": request.headers.get("user-agent"),
        "data": data
    }

    print("===== NEW VISITOR =====")
    print(log)
    print("=======================")

    return jsonify({"status": "ok"})
