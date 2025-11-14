"""Local strategy orchestration helpers for IAMJVP."""

from __future__ import annotations

import re
from typing import Dict, List

RISK_SIGNALS = {
    "delay": "Schedule delays likely—stabilise timelines before committing.",
    "risk": "Explicit risk mentioned—capture mitigation steps in STATUS.md.",
    "outage": "Operational outage referenced—coordinate with incident runbook.",
    "compliance": "Compliance gap noted—loop in governance reviewers.",
    "budget": "Budget pressure detected—prepare cost/benefit summary.",
}

OPPORTUNITY_SIGNALS = {
    "automation": "Automation candidate—consider turning workflow into a tool.",
    "training": "Training opportunity—update user manuals if materialised.",
    "efficiency": "Efficiency gain possible—quantify impact for rollout plan.",
    "expansion": "Expansion theme—validate scope and add to roadmap.",
    "success": "Positive outcome—document lessons in docs/ or STATUS.md.",
}


def _extract_signals(text: str, signal_map: Dict[str, str]) -> List[str]:
    lowered = text.lower()
    results: List[str] = []
    for keyword, message in signal_map.items():
        if re.search(rf"\\b{re.escape(keyword)}\\b", lowered):
            results.append(message)
    return results


def assess_risks(context: str) -> Dict[str, object]:
    """Pull simple risk cues from free-form context."""
    signals = _extract_signals(context, RISK_SIGNALS)
    score = len(signals)
    if score == 0:
        signals.append("No explicit risk keywords detected—validate with stakeholders.")
    return {"score": score, "signals": signals}


def assess_opportunities(context: str) -> Dict[str, object]:
    """Surface opportunity cues from free-form context."""
    signals = _extract_signals(context, OPPORTUNITY_SIGNALS)
    score = len(signals)
    if score == 0:
        signals.append("No clear opportunity keywords—confirm if uplift exists.")
    return {"score": score, "signals": signals}


def orchestrate_strategy(query: str) -> Dict[str, object]:
    """
    Provide a balanced strategic read-out using local heuristics.

    This mirrors the structure from Vertex tutorials but keeps everything in-repo and
    deterministic so contributors can extend it without extra infrastructure.
    """
    risk_view = assess_risks(query)
    opportunity_view = assess_opportunities(query)

    if risk_view["score"] > opportunity_view["score"]:
        strategic_note = "Bias towards caution—address risk items before scaling."
    elif opportunity_view["score"] > risk_view["score"]:
        strategic_note = "Momentum favourable—capture quick wins and assign owners."
    else:
        strategic_note = (
            "Signals balanced—document assumptions and schedule follow-up decision."
        )

    return {
        "status": "success",
        "input": query,
        "risk": risk_view,
        "opportunity": opportunity_view,
        "recommendation": strategic_note,
    }
