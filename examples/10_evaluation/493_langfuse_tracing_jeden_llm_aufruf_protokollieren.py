# Langfuse Tracing -- jeden LLM-Aufruf protokollieren
# Quelle: chapters/10_evaluation.tex (Zeile 493)
# pip install langfuse
from langfuse import Langfuse
import openai

langfuse = Langfuse()

def traced_query(user_message: str) -> str:
    """Ein geloggter LLM-Aufruf mit Langfuse Tracing."""

    trace = langfuse.trace(name="support-ticket-response")

    generation = trace.generation(
        name="chat-completion",
        model="gpt-4o",
        input=[{"role": "user", "content": user_message}],
        metadata={"user_id": 12345},
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_message}],
    )

    generation.update(
        output=response.choices[0].message.content,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_cost": calculate_cost(response),
        },
    )

    return response.choices[0].message.content

