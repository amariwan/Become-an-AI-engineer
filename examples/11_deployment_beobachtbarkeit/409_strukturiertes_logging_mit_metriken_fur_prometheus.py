# Strukturiertes Logging mit Metriken für Prometheus
# Quelle: chapters/11_deployment_beobachtbarkeit.tex (Zeile 409)
import structlog
import time
from prometheus_client import Counter, Histogram, Gauge

# Prometheus-Metriken
LLM_REQUESTS = Counter(
    "llm_requests_total", "Total LLM requests",
    ["model", "status"]
)
LLM_LATENCY = Histogram(
    "llm_latency_seconds", "LLM request latency",
    ["model"], buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
LLM_COST = Counter(
    "llm_cost_total", "Total LLM cost in EUR",
    ["model"]
)

logger = structlog.get_logger()

def monitored_llm_call(model: str, messages: list) -> str:
    """LLM-Aufruf mit Metriken und Logging."""
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=model, messages=messages
        )
        latency = time.time() - start
        tokens = response.usage.total_tokens
        cost = calculate_cost(model, tokens)

        LLM_REQUESTS.labels(model=model, status="success").inc()
        LLM_LATENCY.labels(model=model).observe(latency)
        LLM_COST.labels(model=model).inc(cost)

        logger.info("llm_call_completed",
            model=model,
            latency_s=round(latency, 3),
            tokens=tokens,
            cost_eur=round(cost, 5),
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )

        return response.choices[0].message.content

    except Exception as e:
        latency = time.time() - start
        LLM_REQUESTS.labels(model=model, status="error").inc()
        logger.error("llm_call_failed",
            model=model,
            latency_s=round(latency, 3),
            error=str(e),
        )
        raise

