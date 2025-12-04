# app.py
import os
import json
import base64
from flask import Flask, request, abort
from google.cloud import bigquery

PROJECT = os.environ.get("GCP_PROJECT_ID")
DATASET = os.environ.get("BIGQUERY_DATASET", "llm_security")
TABLE = os.environ.get("BIGQUERY_TABLE", "telemetry")

client = bigquery.Client(project=PROJECT)
table_ref = f"{client.project}.{DATASET}.{TABLE}"

app = Flask(__name__)

def insert_row(record: dict):
    errors = client.insert_rows_json(table_ref, [record])
    if errors:
        app.logger.error("BigQuery insert errors: %s", errors)
        return False
    return True

@app.route("/", methods=["POST"])
def pubsub_push():
    envelope = request.get_json()
    if not envelope:
        abort(400)
    try:
        message = envelope["message"]
        data_b64 = message.get("data")
        if data_b64:
            payload = json.loads(base64.b64decode(data_b64).decode("utf-8"))
        else:
            payload = message.get("attributes", {})
    except Exception as e:
        app.logger.error("Could not parse message: %s", e)
        abort(400)

    # You may want to transform/clean payload for schema compatibility
    success = insert_row(payload)
    if not success:
        abort(500)
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
