# Fehlertolerante LLM-Aufrufe mit Retry und Fallback
# Quelle: chapters/11_deployment_beobachtbarkeit.tex (Zeile 300)
import asyncio
from tenacity import retry, stop_after_attempt,
    wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(
        (openai.RateLimitError, openai.APIConnectionError)),
    reraise=True,
)
async def robust_chat(messages: list[dict]) -> str:
    """LLM-Aufruf mit automatischem Retry und Fallback."""

    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,
                max_tokens=1024,
            ),
            timeout=30.0
        )
        return response.choices[0].message.content

    except openai.RateLimitError:
        # Fallback 1: Modell wechseln
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return response.choices[0].message.content

    except openai.APIConnectionError:
        # Fallback 2: Kleineres Modell
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content

