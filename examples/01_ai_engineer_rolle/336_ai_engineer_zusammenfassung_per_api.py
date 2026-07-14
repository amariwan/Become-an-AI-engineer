# AI Engineer: Zusammenfassung per API
# Quelle: chapters/01_ai_engineer_rolle.tex (Zeile 336)
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class TicketSummary(BaseModel):
    category: str
    sentiment: str
    summary: str
    key_issues: list[str]

def summarize_ticket(ticket_text: str) -> TicketSummary:
    msg = []
    msg.append({"role": "system", "content": "Du bist ein Assistent."})
    msg.append({"role": "user", "content": f"Analysiere: {ticket_text}"})
    resp = client.chat.completions.create(
        model="gpt-4o-mini", messages=msg,
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    text = resp.choices[0].message.content
    return TicketSummary.model_validate_json(text)

t = "Betreff: Rechnung falsch berechnet ..."
s = summarize_ticket(t)
print(f"Kategorie: {s.category}")
print(f"Stimmung: {s.sentiment}")

