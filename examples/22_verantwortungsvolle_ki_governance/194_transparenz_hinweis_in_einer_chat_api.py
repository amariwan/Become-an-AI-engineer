# Transparenz-Hinweis in einer Chat-API
# Quelle: chapters/22_verantwortungsvolle_ki_governance.tex (Zeile 194)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    response = await llm_chat(body["message"])

    return JSONResponse({
        "reply": response,
        "meta": {
            "ai_generated": True,
            "model": "gpt-4o",
            "disclaimer":
                "Diese Antwort wurde von einer KI generiert."
                " Bitte ueberpruefe kritische Informationen."
        }
    })

