# main.py
import os
import time
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .vertex_client import generate_text, analyze_security
from .pubsub_client import publish_telemetry
from .security import hash_prompt, shorten_prompt, enforce_action
from .datadog_client import send_event, send_metric
from dotenv import load_dotenv

load_dotenv()  # optional: load .env during local dev

app = FastAPI(title="LLM Security Guardian API")

class ChatRequest(BaseModel):
    user_id: str
    session_id: str | None = None
    prompt: str
    metadata: dict | None = {}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    t0 = time.time()
    prompt_hash = hash_prompt(req.prompt)
    # 1) Generate via Vertex/Gemini (stub)
    gen = await generate_text(req.prompt)
    response_text = gen["response_text"]
    tokens = gen.get("tokens", 0)
    cost_estimate = gen.get("cost_estimate", 0.0)
    # 2) Security analysis
    analysis = await analyze_security(req.prompt, response_text)
    # 3) Telemetry compose
    telemetry = {
        "timestamp": int(time.time()),
        "user_id": req.user_id,
        "session_id": req.session_id,
        "prompt_hash": prompt_hash,
        "prompt_preview": shorten_prompt(req.prompt),
        "jailbreak_score": analysis.get("jailbreak_score"),
        "threat_type": analysis.get("threat_type"),
        "recommended_action": analysis.get("recommended_action"),
        "pii_leak_risk": analysis.get("pii_leak_risk"),
        "toxicity": analysis.get("toxicity"),
        "tokens": tokens,
        "latency_ms": int((time.time() - t0) * 1000),
        "cost_estimate_usd": cost_estimate,
    }

    # 4) Publish telemetry to pubsub (fire-and-forget)
    try:
        asyncio.get_event_loop().run_in_executor(None, publish_telemetry, telemetry)
    except Exception as e:
        print("pubsub publish error", e)

    # 5) Emit Datadog metrics and events (sampled)
    try:
        send_metric("llm.jailbreak_score", float(telemetry["jailbreak_score"] or 0.0),
                    tags=[f"user:{req.user_id}"])
        if telemetry["jailbreak_score"] and telemetry["jailbreak_score"] > 0.5:
            send_event("LLM high jailbreak score",
                       f"prompt_hash: {telemetry['prompt_hash']}\nscore: {telemetry['jailbreak_score']}",
                       tags=[f"user:{req.user_id}"], alert_type="error")
    except Exception as e:
        print("datadog send error", e)

    # 6) Enforce actions
    action = enforce_action(analysis)
    if action["action_required"]:
        # return a blocked response or sanitized message
        return {
            "response_text": "⚠️ This request has been blocked for safety review.",
            "telemetry": telemetry,
            "action_required": True,
            "analysis": analysis
        }

    return {
        "response_text": response_text,
        "telemetry": telemetry,
        "action_required": False,
        "analysis": analysis
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
