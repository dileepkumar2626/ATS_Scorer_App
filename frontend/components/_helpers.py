from typing import Tuple


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) — dark-mode palette."""
    if score >= 80:
        return "#34D399", "rgba(16,185,129,.12)"
    if score >= 60:
        return "#FBBF24", "rgba(245,158,11,.12)"
    return "#F87171", "rgba(239,68,68,.12)"


def get_score_emoji(score: float) -> str:
    if score >= 90:
        return "🌟"
    if score >= 80:
        return "✅"
    if score >= 70:
        return "👍"
    if score >= 60:
        return "⚠️"
    return "🔴"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    """Return (icon, text_color, background_color) — dark-mode palette."""
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return "🔴", "#F87171", "rgba(239,68,68,.1)"
    if level == "medium":
        return "🟡", "#FBBF24", "rgba(245,158,11,.1)"
    return "🟢", "#34D399", "rgba(16,185,129,.1)"
