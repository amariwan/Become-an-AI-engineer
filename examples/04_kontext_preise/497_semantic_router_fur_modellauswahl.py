# Semantic Router fur Modellauswahl
# Quelle: chapters/04_kontext_preise.tex (Zeile 497)
def route_query(query: str) -> str:
    """Entscheide, welches Modell fur diese Query optimal ist."""
    prompt = (
        "Klassifiziere die folgende User-Anfrage in eine Kategorie: "
        "'simple' (1-2 Satze, Faktenabfrage, Extraktion), "
        "'complex' (Reasoning, Analyse, Multi-Step), "
        "'creative' (Brainstorming, Textgenerierung).\n\n"
        f"Anfrage: {query}\n\n"
        "Antworte nur mit der Kategorie."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0.0,
    )
    category = response.choices[0].message.content.strip()

    routing = {
        "simple": "gpt-4o-mini",
        "complex": "gpt-4o",
        "creative": "claude-sonnet-4",
    }
    return routing.get(category, "gpt-4o-mini")

# Nutzung in der API
model = route_query(user_query)
response = call_model(model, user_query)

