# security.py
import hashlib
from typing import Dict, Any

def hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

def shorten_prompt(prompt: str, length=200) -> str:
    return (prompt[:length] + "...") if len(prompt) > length else prompt

def enforce_action(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determine final action based on analysis.
    Returns dict with action and message.
    """
    score = analysis.get("jailbreak_score", 0.0)
    recommended = analysis.get("recommended_action", "REVIEW")
    blocked = recommended == "BLOCK" or score >= 0.8
    return {
        "action_required": blocked,
        "recommended_action": recommended
    }
