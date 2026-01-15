from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ==========================
# IN-MEMORY LOG (VIBE MODE)
# ==========================
FINGERPRINT_LOGS = []

# ==========================
# Demo data
# ==========================
posts = [
    {
        "title": "Understanding Civil Law Basics",
        "excerpt": "Key principles of civil law and how they affect daily life.",
        "category": "Civil Law",
        "author": "Jane Doe",
        "date": "2025-01-10",
    }
]

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

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

    # LƯU TẠM RAM
    FINGERPRINT_LOGS.append(fp)

    # LOG RA CONSOLE (XEM TRONG VERCEL LOGS)
    print("📌 FINGERPRINT RECEIVED")
    print(fp)

    return jsonify({"status": "ok"})

# ==========================
# VIEW FINGERPRINT LIVE
# ==========================
@app.route("/debug/fingerprints")
def debug_fingerprints():
    return jsonify({
        "count": len(FINGERPRINT_LOGS),
        "items": FINGERPRINT_LOGS[-10:]  # xem 10 cái gần nhất
    })
