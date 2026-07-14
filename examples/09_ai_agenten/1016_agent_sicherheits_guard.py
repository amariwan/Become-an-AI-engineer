# Agent-Sicherheits-Guard
# Quelle: chapters/09_ai_agenten.tex (Zeile 1016)
class SafetyGuard:
    def __init__(self, max_steps: int = 20,
                 max_tokens_per_step: int = 4000,
                 max_cost_per_run: float = 1.0):
        self.max_steps = max_steps
        self.max_tokens = max_tokens_per_step
        self.max_cost = max_cost_per_run
        self.step_count = 0
        self.total_cost = 0.0

    def check_before_tool(self, tool_name: str, args: dict) -> bool:
        self.step_count += 1
        if self.step_count > self.max_steps:
            raise RuntimeError("Max steps exceeded")

        # Blacklist gefaehrlicher Tools
        if tool_name in {"execute_shell", "delete_file", "send_email"}:
            return False  # Human-in-the-Loop erforderlich

        # Whitelist erlaubter Domains
        if tool_name == "http_request":
            url = args.get("url", "")
            if not url.startswith("https://api.company-intern.com"):
                return False

        return True

    def check_after_tool(self, result: str) -> str:
        # Tool-Ergebnis auf schädliche Anweisungen scannen
        injection_patterns = [
            "ignore previous", "ignore all", "system prompt",
        ]
        for pattern in injection_patterns:
            if pattern.lower() in result.lower():
                return "[Safety: Output blocked - injection detected]"

        # Groesse begrenzen
        max_chars = 10000
        return result[:max_chars]

