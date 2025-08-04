from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Replace with your actual credentials from Meta
ACCESS_TOKEN = 'YOUR_WHATSAPP_ACCESS_TOKEN'
PHONE_NUMBER_ID = 'YOUR_PHONE_NUMBER_ID'
VERIFY_TOKEN = 'your_webhook_verify_token'

# Webhook verification endpoint (Meta checks this when you register the webhook)
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args["hub.challenge"], 200
        return "Verification token mismatch", 403
    return "Hello World", 200

# Message processing endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry["changes"]:
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    phone_number = message["from"]
                    msg_body = message["text"]["body"]

                    # Basic response logic
                    if "hi" in msg_body.lower():
                        reply = "Hello! How can I help you today?"
                    else:
                        reply = f"You said: {msg_body}"

                    send_message(phone_number, reply)
    return "OK", 200

def send_message(recipient, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Sent message:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(port=5000)
