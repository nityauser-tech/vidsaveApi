from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

VIDSSAVE_URL = "https://api.vidssave.com/api/contentsite_api/media/parse"

HEADERS = {
    "user-agent": "Mozilla/5.0",
    "content-type": "application/x-www-form-urlencoded"
}

CREDIT_INFO = {
    "credit": "anshapis",
    "developer": "anshapis"
}

@app.route("/")
def home():
    return jsonify({
        "message": "API running",
        "endpoint": "/parse?link=URL",
        **CREDIT_INFO
    })

@app.route("/parse")
def parse_video():
    link = request.args.get("link")

    if not link:
        return jsonify({"error": "Missing link", **CREDIT_INFO}), 400

    encoded_link = urllib.parse.quote_plus(link)

    data = f"auth=20250901majwlqo&domain=api-ak.vidssave.com&origin=cache&link={encoded_link}"

    try:
        r = requests.post(VIDSSAVE_URL, headers=HEADERS, data=data)
        result = r.json()
        result.update(CREDIT_INFO)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
