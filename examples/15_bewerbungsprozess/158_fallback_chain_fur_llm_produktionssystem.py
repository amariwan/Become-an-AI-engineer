# Fallback-Chain für LLM-Produktionssystem
# Quelle: chapters/15_bewerbungsprozess.tex (Zeile 158)
class FallbackChain:
    """Mehrstufige Fallback-Strategie fuer LLM-Calls."""

    def __init__(self):
        self.providers = [
            {"name": "primary", "model": "claude-sonnet-4",
             "client": anthropic.Client()},
            {"name": "backup", "model": "gpt-4o",
             "client": openai.Client()},
            {"name": "fallback", "model": "gpt-4o-mini",
             "client": openai.Client()},
        ]
        self.cache_ttl = 300

    async def execute(self, prompt: str,
                      timeout: float = 10.0) -> dict:
        errors = []

        for provider in self.providers:
            try:
                response = await asyncio.wait_for(
                    provider["client"].complete(prompt),
                    timeout=timeout,
                )
                return {
                    "response": response,
                    "provider": provider["name"],
                    "model": provider["model"],
                    "fallback_used": len(errors) > 0,
                }
            except Exception as e:
                errors.append({
                    "provider": provider["name"],
                    "error": str(e),
                })
                continue

        # Alle Provider ausgefallen -> Degraded Mode
        return {
            "response": "Service temporarily unavailable. "
                        "Please try again.",
            "provider": None,
            "model": None,
            "errors": errors,
            "degraded": True,
        }

