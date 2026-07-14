# Observability-Layer im Portfolio
# Quelle: chapters/15_bewerbungsprozess.tex (Zeile 226)
class ObservabilityLayer:
    """Zeigt, dass Monitoring und Debugging implementiert sind."""

    def instrument(self, app):
        @app.middleware("http")
        async def trace_request(request, call_next):
            trace_id = str(uuid.uuid4())
            request.state.trace_id = trace_id

            # Startzeit
            start = time.monotonic()

            try:
                response = await call_next(request)
            except Exception as e:
                # Fehler mit Kontext loggen
                logger.error({
                    "trace_id": trace_id,
                    "error": str(e),
                    "path": request.url.path,
                    "user": request.headers.get("x-user-id"),
                })
                raise

            # Latenz tracken
            latency = time.monotonic() - start
            METRICS_HISTOGRAM.labels(
                path=request.url.path,
                status=response.status_code,
            ).observe(latency)

            # Response loggen (PII-free)
            logger.info({
                "trace_id": trace_id,
                "latency_ms": int(latency * 1000),
                "status": response.status_code,
                "tokens": response.headers.get("x-tokens-used"),
            })

            return response

