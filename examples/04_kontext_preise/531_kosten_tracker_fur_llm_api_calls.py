# Kosten-Tracker fur LLM-API-Calls
# Quelle: chapters/04_kontext_preise.tex (Zeile 531)
import time
from collections import defaultdict

class CostTracker:
    """Trackt API-Kosten pro Modell und Tag."""

    def __init__(self, budget_monthly: float = 100.0):
        self.usage: dict[str, list[dict]] = defaultdict(list)
        self.budget = budget_monthly

    def track(self, model: str, input_tokens: int,
              output_tokens: int) -> float:
        pricing = MODEL_PRICING[model]
        cost = (input_tokens / 1_000_000
                * pricing.input_price_per_million
                + output_tokens / 1_000_000
                * pricing.output_price_per_million)
        self.usage[model].append({
            "cost": cost,
            "timestamp": time.time(),
        })
        return cost

    def monthly_cost(self) -> float:
        """Gesamtkosten des aktuellen Monats."""
        month_ago = time.time() - 30 * 24 * 3600
        total = 0.0
        for model, calls in self.usage.items():
            for call in calls:
                if call["timestamp"] > month_ago:
                    total += call["cost"]
        return total

    def check_budget(self) -> str | None:
        """Warnung bei Budget-uberschreitung."""
        used = self.monthly_cost()
        if used > self.budget * 0.8:
            return (
                f"WARNUNG: {used:.2f} $ von {self.budget} $ "
                f"verbraucht ({used/self.budget:.0%})"
            )
        return None

