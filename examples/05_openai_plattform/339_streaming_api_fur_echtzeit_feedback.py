# Streaming-API für Echtzeit-Feedback
# Quelle: chapters/05_openai_plattform.tex (Zeile 339)
# Server-side (FastAPI)
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import openai

async def stream_response(user_message):
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )
    async for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

@app.get("/chat")
def chat(user_message: str):
    return StreamingResponse(
        stream_response(user_message), media_type="text/plain"
    )

