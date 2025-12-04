# vertex_client.py
import os
import asyncio
from typing import Dict, Any

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

async def generate_text(prompt: str) -> Dict[str, Any]:
    """
    Replace this stub with real Vertex AI calls using google-cloud-aiplatform SDK.
    For hackathon prototype we simulate generation.
    """
    await asyncio.sleep(0.15)
    return {
        "response_text": f"SIMULATED RESPONSE to: {prompt}",
        "tokens": max(1, len(prompt.split())),
        "cost_estimate": 0.0005
    }

async def analyze_security(prompt: str, response: str) -> Dict[str, Any]:
    """
    Call Gemini/Vertex AI with a structured-output instruction to return JSON security analysis.
    For prototyping we include a simple heuristic.
    """
    await asyncio.sleep(0.08)
    low = 0.01
    high = 0.95
    score = high if ("ignore previous" in prompt.lower() or "dan" in prompt.lower()) else low
    threat = "JAILBREAK" if score > 0.5 else "NONE"
    recommended = "BLOCK" if score > 0.7 else ("REVIEW" if score > 0.5 else "ALLOW")
    return {
        "jailbreak_score": float(score),
        "threat_type": threat,
        "pii_leak_risk": 0.01,
        "toxicity": 0.02,
        "extracted_indicators": [],
        "recommended_action": recommended
    }
