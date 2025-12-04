# app.py
import os
import json
import time
from flask import Flask, request, abort
import requests

DD_API_KEY = os.environ.get("DATADOG_API_KEY")
DD_SITE = os.environ.get("DATADOG_SITE", "datadoghq.com")
DD_SERVICE = os.environ.get("DATADOG_SERVICE", "llm-security-guardian")

app = Flask(__name__)

def post_datadog_event(title, text, tags=None, alert_type="info"):
    url = f"https://api.{DD_SITE}/api/v1/events?api_key={DD_API_KEY}"
    body = {"title": title, "text": text, "tags": tags or [], "alert_type": alert_type, "date_happened": int(time.time())}
    try:
        r = requests.post(url, json=body, timeout=5)
        r.raise_for_status()
    except Exception as e:
        app.logger.error("Datadog event failed: %s", e)

@app.route("/", methods=["POST"])
def pubsub_push():
    """
    This endpoint can be used with Pub/Sub push subscription.
    Pub/Sub will POST JSON with 'message' field encoded in base64.
    """
    envelope = request.get_json()
    if not envelope:
        abort(400)
    # Pull message data:
    try:
        message = envelope["message"]
        data_b64 = message.get("data")
        if data_b64:
            import base64
            payload = json.loads(base64.b64decode(data_b64).decode("utf-8"))
        else:
            payload = message.get("attributes", {})
    except Exception as e:
        app.logger.error("Could not parse Pub/Sub message: %s", e)
        abort(400)

    # Forward to Datadog:
    title = f"LLM Telemetry - {payload.get('threat_type','NONE')}"
    text = json.dumps(payload, indent=2)
    alert_type = "error" if payload.get("jailbreak_score", 0) > 0.5 else "info"
    post_datadog_event(title, text, tags=[f"service:{DD_SERVICE}"], alert_type=alert_type)

    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
