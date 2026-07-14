# Health-Check mit API-Readiness
# Quelle: chapters/11_deployment_beobachtbarkeit.tex (Zeile 623)
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/health")
async def health():
    """Standard-Healthcheck."""
    return {"status": "ok"}

@app.get("/ready")
async def readiness():
    """Readiness-Check: Testet, ob die LLM-API erreichbar ist."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": "Bearer sk-..."},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user",
                                  "content": "ping"}],
                    "max_tokens": 1,
                },
            )
            if resp.status_code == 200:
                return {"status": "ready", "llm": "reachable"}
    except Exception:
        pass
    return {"status": "not_ready", "llm": "unreachable"}

