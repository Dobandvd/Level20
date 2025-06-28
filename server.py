from flask import Flask, request, jsonify
import os
import logging
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# PayPal webhook verification token (set in your PayPal settings)
VERIFY_TOKEN = os.getenv("PAYPAL_VERIFY_TOKEN")

# Basic Flask app
app = Flask(__name__)

# Dummy in-memory database to track who paid
wagers = {}

# Logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def health_check():
    return "✅ Flask server running!"

@app.route("/paypal-webhook", methods=["POST"])
def paypal_webhook():
    # PayPal sends webhook events here
    data = request.json

    # Optional: Add basic logging for debug
    logging.info("Received PayPal webhook: %s", data)

    # Step 1: Verify event type
    event_type = data.get("event_type", "")
    if event_type != "PAYMENT.CAPTURE.COMPLETED":
        return jsonify({"status": "ignored", "reason": "not a completed payment"}), 200

    # Step 2: Extract custom ID or payer email (depends on how you set PayPal link up)
    payer_email = data.get("resource", {}).get("payer", {}).get("email_address", "unknown")
    custom_id = data.get("resource", {}).get("custom_id", "wager1")  # Optional, if using custom_id in payment

    # Step 3: Mark user as paid
    if custom_id not in wagers:
        wagers[custom_id] = []

    wagers[custom_id].append(payer_email)

    logging.info(f"[WAGER] {payer_email} has paid for {custom_id}")
    return jsonify({"status": "success", "wager": custom_id, "payer": payer_email}), 200


# Run Flask app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
