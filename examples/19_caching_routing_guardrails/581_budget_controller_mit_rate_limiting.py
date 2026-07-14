# Budget-Controller mit Rate-Limiting
# Quelle: chapters/19_caching_routing_guardrails.tex (Zeile 581)
import time
from collections import defaultdict

class BudgetController:
    def __init__(self):
        self.daily_budget = 100.0    # EUR pro Tag (global)
        self.user_budget = 5.0       # EUR pro Tag (per User)
        self.rate_limit = 60         # Requests pro Minute (per User)
        self.user_costs = defaultdict(float)
        self.user_requests = defaultdict(list)
        self.total_cost = 0.0

    def check_request(self, user_id: str,
                      estimated_cost: float) -> dict:
        now = time.time()

        # 1. Globales Budget
        if self.total_cost + estimated_cost > self.daily_budget:
            return {"allowed": False,
                    "reason": "Globales Tagesbudget erschöpft"}

        # 2. User-Budget
        if (self.user_costs[user_id] + estimated_cost
                > self.user_budget):
            return {"allowed": False,
                    "reason": "User-Tagesbudget erschöpft"}

        # 3. Rate-Limit
        minute_ago = now - 60
        self.user_requests[user_id] = [
            t for t in self.user_requests[user_id]
            if t > minute_ago
        ]
        if len(self.user_requests[user_id]) >= self.rate_limit:
            return {"allowed": False,
                    "reason": "Rate-Limit erreicht (60/min)"}

        # Genehmigt
        self.user_requests[user_id].append(now)
        return {"allowed": True}

    def record_cost(self, user_id: str, cost: float):
        self.user_costs[user_id] += cost
        self.total_cost += cost

    def budget_status(self) -> dict:
        return {
            "total_spent": self.total_cost,
            "total_budget": self.daily_budget,
            "remaining": self.daily_budget - self.total_cost,
            "active_users": len(self.user_costs),
            "top_spenders": sorted(
                self.user_costs.items(),
                key=lambda x: -x[1],
            )[:5],
        }

# Nutzung im Request-Handler
budget = BudgetController()

def handle_request(user_id: str, query: str):
    estimated = estimate_cost(query)
    check = budget.check_request(user_id, estimated)

    if not check["allowed"]:
        return {"error": check["reason"]}

    response = call_llm("gpt-4o-mini", query)
    actual_cost = calculate_cost(response)
    budget.record_cost(user_id, actual_cost)

    return {"response": response, "cost": actual_cost}

