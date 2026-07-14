# Safety-Monitoring mit Metrik-Export
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 403)
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

class SafetyMonitor:
    """Protokolliert und analysiert Safety-Vorfalle in LLM-Calls."""

    def __init__(self):
        self.events: list[dict] = []
        self.daily_counts: dict[str, int] = defaultdict(int)

    def log_call(self, prompt: str, response: str,
                 safety_result: dict, latency_ms: float) -> None:
        """Jeden LLM-Call mit Safety-Status loggen."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "prompt_length": len(prompt),
            "response_length": len(response),
            "is_safe": safety_result.get("is_safe", True),
            "issues": safety_result.get("issues", []),
            "latency_ms": latency_ms,
        }
        self.events.append(event)
        self.daily_counts["total"] += 1
        if not event["is_safe"]:
            self.daily_counts["flagged"] += 1

    def safety_rate(self, hours: int = 24) -> float:
        """Safety-Quote der letzten N Stunden."""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [
            e for e in self.events
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]
        if not recent:
            return 1.0
        safe = sum(1 for e in recent if e["is_safe"])
        return safe / len(recent)

    def top_issues(self, n: int = 5) -> list[tuple[str, int]]:
        """Haufigste Safety-Issues."""
        counts: dict[str, int] = defaultdict(int)
        for event in self.events:
            for issue in event.get("issues", []):
                counts[issue["type"]] += 1
        return sorted(counts.items(),
                      key=lambda x: x[1], reverse=True)[:n]

    def alert_if_needed(self, threshold: float = 0.95) -> str | None:
        """Alert, wenn Safety-Rate unter Schweilenwert fallt."""
        rate = self.safety_rate(hours=1)
        if rate < threshold:
            return (
                f"ALERT: Safety-Rate {rate:.1%} unter "
                f"Schwelle {threshold:.1%} in der letzten Stunde!"
            )
        return None

# Nutzung
monitor = SafetyMonitor()
# Wurde bei jedem LLM-Call aufgerufen
monitor.log_call(
    prompt="Kundendaten: Hans Meier, h.meier@email.de",
    response="Vielen Dank fur Ihre Anfrage.",
    safety_result={"is_safe": True, "issues": []},
    latency_ms=234,
)

