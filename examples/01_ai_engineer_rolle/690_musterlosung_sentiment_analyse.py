# Musterlösung: Sentiment-Analyse
# Quelle: chapters/01_ai_engineer_rolle.tex (Zeile 690)
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class FeedbackResult(BaseModel):
    sentiment: str  # "positiv" | "neutral" | "negativ"
    confidence: float
    reason: str

def analyze_feedback(text: str) -> dict:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Klassifiziere das Feedback als positiv, neutral oder negativ. "
                            "Antworte als JSON: sentiment, confidence, reason."},
                {"role": "user", "content": text},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        result = FeedbackResult.model_validate_json(
            resp.choices[0].message.content
        )
        return {
            "input": text[:40] + "...",
            "result": result.model_dump(),
            "tokens": resp.usage.total_tokens,
        }
    except Exception as e:
        return {"input": text[:40], "error": str(e)}

feedbacks = [
    "Der Versand war super schnell, aber die Verpackung war beschädigt.",
    "Ich warte seit drei Wochen auf meine Bestellung. Nie wieder!",
    "Alles perfekt. Genau wie beschrieben. Gerne wieder.",
    "Die Qualität ist okay für den Preis. Nichts besonderes.",
    "Der Kundenservice hat mein Problem sofort gelöst. Fantastisch!",
]

for fb in feedbacks:
    result = analyze_feedback(fb)
    print(f"{result['input']}\n  -> {result.get('result', result.get('error'))}\n")

