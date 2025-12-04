# pubsub_client.py
from google.cloud import pubsub_v1
import os
import json

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
PUBSUB_TOPIC = os.environ.get("PUBSUB_TELEMETRY_TOPIC")

publisher = pubsub_v1.PublisherClient()

def publish_telemetry(record: dict):
    """
    Publish telemetry JSON to the configured Pub/Sub topic.
    """
    if not PUBSUB_TOPIC:
        # fallback: no pubsub configured
        return
    data = json.dumps(record).encode("utf-8")
    future = publisher.publish(PUBSUB_TOPIC, data)
    # optionally block or add callback in production
    future.result(timeout=10)
