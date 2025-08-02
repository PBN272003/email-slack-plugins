from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

@app.route("/send_slack_message", methods=["POST"])
def send_slack_message():
    data = request.get_json()

    channel = data.get("channel")  
    text = data.get("message") or data.get("text")

    if not channel or not text:
        return jsonify({"error": "channel and message are required"}), 400

    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-type": "application/json"
    }

    payload = {
        "channel": channel,
        "text": text
    }

    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    response_data = response.json()
    print("Slack API JSON response:", response_data)

    if response.status_code == 200 and response_data.get("ok"):
        return jsonify({"message": "Message sent successfully!"})
    else:
        return jsonify({"error": "Failed to send message", "details": response_data}), 500

@app.route("/get_user_info", methods=["POST"])
def get_user_info():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.get(
        "https://slack.com/api/users.lookupByEmail",
        headers=headers,
        params={"email": email}
    )

    response_data = response.json()
    print("Slack API Response:", response_data)

    if response.status_code == 200 and response_data.get("ok"):
        return jsonify({"user": response_data["user"]})
    else:
        return jsonify({"error": "Failed to retrieve user", "details": response_data}), 500

@app.route("/openapi_getuser.yaml", methods=["GET"])
def serve_openapi_getuser():
    return send_file("openapi_getuser.yaml", mimetype="text/yaml")

@app.route("/openapi.yaml", methods=["GET"])
def serve_openapi():
    return send_file("openapi.yaml", mimetype="text/yaml")

if __name__ == "__main__":
    app.run(port=5005, debug=True)
