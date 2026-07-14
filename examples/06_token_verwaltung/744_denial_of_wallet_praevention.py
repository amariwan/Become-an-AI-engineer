# Denial-of-Wallet-Praevention
# Quelle: chapters/06_token_verwaltung.tex (Zeile 744)
class BudgetGuard:
    def __init__(self, max_daily_cost: float = 100.0):
        self.max_daily_cost = max_daily_cost
        self.tracker = CostTracker()

    def check_budget(self) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        cost = self.tracker.daily_cost(today)
        return cost < self.max_daily_cost

    def guard(self, func):
        """Decorator: Blockiert API-Calls, wenn Budget erreicht."""
        def wrapper(*args, **kwargs):
            if not self.check_budget():
                raise RuntimeError(
                    f"Daily budget {self.max_daily_cost}$ reached"
                )
            return func(*args, **kwargs)
        return wrapper

