# Streaming-Response für Echtzeit-Feedback
# Quelle: chapters/11_deployment_beobachtbarkeit.tex (Zeile 265)
from fastapi.responses import StreamingResponse

async def stream_chat(user_input: str):
    """Streaming-Endpoint mit SSE (Server-Sent Events)."""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        stream=True,
    )

    async def generate():
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/chat/stream")
async def chat_stream(request: Request, user_input: str):
    return await stream_chat(user_input)

