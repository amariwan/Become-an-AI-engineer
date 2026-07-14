# FastAPI-Microservice mit Caching und Rate Limiting
# Quelle: chapters/11_deployment_beobachtbarkeit.tex (Zeile 156)
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import openai
import hashlib
import time
from typing import Optional

app = FastAPI(title="AI-Assistant API", version=1.0.0)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

cache = {}

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, user_input: str):
    """Chat-Endpoint mit Caching und Kosten-Tracking."""

    cache_key = hashlib.md5(user_input.encode()).hexdigest()
    if cache_key in cache and time.time() - cache[cache_key]["ts"] < 300:
        return {"response": cache[cache_key]["response"], "cached": True}

    try:
        start = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": user_input},
            ],
            temperature=0.1,
            max_tokens=1024,
        )
        latency_ms = (time.time() - start) * 1000

        result = response.choices[0].message.content

        cache[cache_key] = {
            "response": result,
            "ts": time.time(),
        }

        print(f"[METRIC] latency={latency_ms:.0f}ms tokens={response.usage.total_tokens}")

        return {"response": result, "cached": False, "latency_ms": latency_ms}

    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate Limit erreicht.")
    except openai.APIConnectionError:
        raise HTTPException(status_code=503, detail="KI-Dienst nicht verfuegbar.")

@app.get("/health")
async def health():
    """Health-Check fuer Load Balancer."""
    return {"status": "healthy", "model": "gpt-4o-mini"}

