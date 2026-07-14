# Chain-of-Thought
# Quelle: chapters/07_prompt_design.tex (Zeile 241)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "system",
        "content": (
            "Denke Schritt fuer Schritt nach. "
            "Erklaere dein Vorgehen, dann das finale Ergebnis."
        )
    }, {
        "role": "user",
        "content": (
            "Ein Agent bearbeitet 40 Tickets/Tag. "
            "5% der Tickets brauchen 30 Min, 95% brauchen 10 Min. "
            "Wie viele kritische Tickets schafft er?"
        )
    }],
)

