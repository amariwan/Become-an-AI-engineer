# Kosten-Tracker für LLM-API-Aufrufe
# Quelle: chapters/21_mlops_modelllebenszyklus.tex (Zeile 294)
import time
from dataclasses import dataclass, field

@dataclass
class CostTracker:
    budget_limit: float
    current_cost: float = 0.0
    alerts: list = field(default_factory=list)

    def track(self, model: str, prompt_tokens: int,
              completion_tokens: int, prices: dict) -> None:
        price = prices.get(model, 0)
        cost = (prompt_tokens * price["input"]
                + completion_tokens * price["output"]) / 1_000_000
        self.current_cost += cost
        ratio = self.current_cost / self.budget_limit
        if ratio >= 0.8:
            self.alerts.append(
                f"Warnung: {ratio:.0%} des Budgets erreicht"
            )

    def over_budget(self) -> bool:
        return self.current_cost >= self.budget_limit

