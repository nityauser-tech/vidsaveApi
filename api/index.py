from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

VIDSSAVE_URL = "https://api.vidssave.com/api/contentsite_api/media/parse"

HEADERS = {
    "sec-ch-ua-platform": "\"Android\"",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
    "dnt": "1",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua-mobile": "?1",
    "accept": "*/*",
    "origin": "https://vidssave.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://vidssave.com/",
    "accept-language": "en-GB,en;q=0.9"
}

CREDIT_INFO = {
    "credit": "anshapis",
    "developer": "anshapis"
}

@app.route("/")
def home():
    return jsonify({
        "message": "Video Parser API running on Vercel",
        "endpoint": "/parse?link=URL",
        **CREDIT_INFO
    })

@app.route("/parse")
def parse_video():
    link = request.args.get("link")

    if not link:
        return jsonify({"error": "Missing link parameter", **CREDIT_INFO}), 400

    encoded_link = urllib.parse.quote_plus(link)

    data = f"auth=20250901majwlqo&domain=api-ak.vidssave.com&origin=cache&link={encoded_link}"

    try:
        response = requests.post(VIDSSAVE_URL, headers=HEADERS, data=data)
        response_data = response.json()
        response_data.update(CREDIT_INFO)
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e), **CREDIT_INFO}), 500


# Vercel handler
def handler(request, context):
    return app(request.environ, start_response=lambda status, headers: None)
