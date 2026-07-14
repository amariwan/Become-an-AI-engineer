# Content-Moderation vor dem API-Call
# Quelle: chapters/05_openai_plattform.tex (Zeile 600)
def moderated_query(user_input: str):
    # Schritt 1: Input prüfen
    moderation = client.moderations.create(input=user_input)
    if moderation.results[0].flagged:
        return {"error": "Input violates content policy"}

    # Schritt 2: API-Call nur bei Clean-Input
    response = client.chat.completions.create(...)
    # Schritt 3: Auch den Output prüfen
    output_mod = client.moderations.create(
        input=response.choices[0].message.content
    )
    if output_mod.results[0].flagged:
        return {"error": "Output flagged for review"}

    return response

