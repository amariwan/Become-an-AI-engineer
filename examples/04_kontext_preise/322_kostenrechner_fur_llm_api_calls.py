# Kostenrechner für LLM-API-Calls
# Quelle: chapters/04_kontext_preise.tex (Zeile 322)
from dataclasses import dataclass

@dataclass
class ModelPricing:
    input_price_per_million: float
    output_price_per_million: float

MODEL_PRICING = {
    "gpt-4o": ModelPricing(2.50, 10.00),
    "gpt-4o-mini": ModelPricing(0.15, 0.60),
    "claude-sonnet-4": ModelPricing(3.00, 15.00),
    "gemini-flash-2.5": ModelPricing(0.08, 0.30),
}

def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    daily_queries: int = 1,
) -> dict:
    """Berechne Kosten fur einen oder mehrere API-Calls."""
    pricing = MODEL_PRICING[model]

    input_cost = (input_tokens / 1_000_000
                  * pricing.input_price_per_million)
    output_cost = (output_tokens / 1_000_000
                   * pricing.output_price_per_million)
    per_query = input_cost + output_cost

    return {
        "model": model,
        "cost_per_query": round(per_query, 5),
        "cost_per_1k_queries": round(per_query * 1000, 2),
        "cost_per_10k_queries": round(per_query * 10000, 2),
        "cost_monthly_30d": round(per_query * daily_queries * 30, 2),
    }

# Beispiel: Kosten fur ein RAG-System
costs = estimate_cost(
    "gpt-4o-mini",
    input_tokens=8_000,   # System + RAG-Kontext
    output_tokens=500,     # Antwort
    daily_queries=10_000,
)
print(f"Pro Query:   {costs['cost_per_query']} $")
print(f"Pro Monat:   {costs['cost_monthly_30d']} $")

