from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ==========================
# IN-MEMORY LOG (DEBUG ONLY)
# ==========================
FINGERPRINT_LOGS = []

@app.route("/")
def index():
    return render_template("index.html")

# ==========================
# RECEIVE FINGERPRINT
# ==========================
@app.route("/api/fingerprint", methods=["POST"])
def api_fingerprint():
    data = request.get_json(silent=True) or {}

    fp = {
        "time": datetime.utcnow().isoformat() + "Z",
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "ua": request.headers.get("User-Agent"),
        "data": data
    }

    # LƯU RAM (DEBUG)
    FINGERPRINT_LOGS.append(fp)

    # ===== LOG RA NGOÀI =====
    print("========== NEW VISITOR ==========")
    print(fp)
    print("=================================")

    return jsonify({"status": "ok"})

# ==========================
# VIEW LOG LIVE (DEBUG)
# ==========================
@app.route("/debug/fingerprints")
def debug_fingerprints():
    return jsonify({
        "count": len(FINGERPRINT_LOGS),
        "items": FINGERPRINT_LOGS[-10:]
    })
