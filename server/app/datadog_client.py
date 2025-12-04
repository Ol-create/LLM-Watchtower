# datadog_client.py
import os
import time
import requests

DD_API_KEY = os.environ.get("DATADOG_API_KEY")
DD_SITE = os.environ.get("DATADOG_SITE", "datadoghq.com")
DD_SERVICE = os.environ.get("DATADOG_SERVICE", "llm-security-guardian")

def send_event(title: str, text: str, tags: list[str] = None, alert_type: str = "info"):
    url = f"https://api.{DD_SITE}/api/v1/events?api_key={DD_API_KEY}"
    body = {
        "title": title,
        "text": text,
        "tags": tags or [f"service:{DD_SERVICE}"],
        "alert_type": alert_type,
        "date_happened": int(time.time())
    }
    try:
        resp = requests.post(url, json=body, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Datadog event failed", e)
        return None

def send_metric(metric_name: str, value: float, tags: list[str] = None):
    url = f"https://api.{DD_SITE}/api/v1/series?api_key={DD_API_KEY}"
    point = [[int(time.time()), value]]
    payload = {
        "series": [
            {
                "metric": metric_name,
                "points": point,
                "type": "gauge",
                "tags": tags or [f"service:{DD_SERVICE}"]
            }
        ]
    }
    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Datadog metric failed", e)
        return None
