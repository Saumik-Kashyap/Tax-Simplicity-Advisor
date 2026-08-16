"""
app.py
Flask backend for the Informal Economy Tax-Simplicity Advisor.

Serves the HTML/CSS/JS frontend (templates/index.html) and exposes
POST /api/analyze, which runs the REAL Python logic (extractor.py +
rules_engine.py) and returns JSON. The frontend calls this via fetch()
instead of recalculating anything in JavaScript.
"""

from flask import Flask, render_template, request, jsonify

from extractor import extract_business_profile
from rules_engine import build_full_report

app = Flask(__name__, template_folder=".")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tax-guide")
def tax_guide():
    return render_template("tax-guide.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No business description provided."}), 400

    profile = extract_business_profile(text)
    report = build_full_report(profile)

    # Flatten into a clean JSON payload for the frontend
    response = {
        "profile": {
            "revenue": profile.get("annual_revenue"),
            "type": profile.get("business_type"),
            "state": profile.get("state"),
            "isWoman": profile.get("is_woman_owned", False),
            "isScSt": profile.get("is_sc_st", False),
            "isNew": profile.get("is_new_business", False),
        },
        "gst": report["gst"],
        "presumptiveTax": report["presumptive_tax"],
        "udyamTier": report["udyam_tier"],
        "benefits": [
            {"name": b["name"], "description": b["description"]}
            for b in report["benefits"]
        ],
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
