# Cost-Awareness im Portfolio nachweisen
# Quelle: chapters/15_bewerbungsprozess.tex (Zeile 110)
class ProductionAwarePipeline:
    """Zeigt, dass Kosten, Latenz und Fehler behandelt werden."""

    def __init__(self):
        self.cache = SemanticCache(threshold=0.92)
        self.router = SemanticRouter()
        self.budget = BudgetController()
        self.metrics = MetricsCollector()

    async def handle(self, query: str, user_id: str) -> dict:
        start = time.monotonic()

        # 1. Budget-Check
        if not self.budget.check_request(user_id, 0.005):
            return {"error": "Budget limit reached",
                    "status": 429}

        # 2. Cache-Lookup (0-Latenz bei Hit)
        cached, score = self.cache.lookup(query)
        if cached:
            self.metrics.record(user_id, "cache_hit", 0.0)
            return {"response": cached, "cached": True}

        # 3. Intent-Routing
        route = self.router.route(query)
        response = await call_provider(route["model"], query)

        # 4. Kosten tracken
        cost = calculate_cost(response, route["model"])
        self.budget.record_cost(user_id, cost)
        self.metrics.record(user_id, "llm_call", cost)

        # 5. Cache-schreiben (je nach Intent)
        if route["intent"] not in ("personal", "sensitive"):
            self.cache.store(query, response)

        elapsed = time.monotonic() - start
        self.metrics.record_latency(user_id, elapsed)

        return {"response": response, "cached": False,
                "latency_ms": int(elapsed * 1000)}

