# Confidence-Scoring mit Logprobs für Halluzinations-Erkennung
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 132)
def estimate_hallucination_risk(response) -> float:
    """Berechne Halluzinations-Risiko basierend auf Logprobs."""
    logprobs = response.choices[0].logprobs

    if not logprobs:
        return 0.0

    # Durchschnittliche Token-Wahrscheinlichkeit
    token_probs = [
        np.exp(token.logprob)
        for token in logprobs.content
    ]
    avg_confidence = np.mean(token_probs)

    # Niedrige Confidence = hohes Halluzinationsrisiko
    risk_score = 1.0 - avg_confidence
    return max(0.0, min(1.0, risk_score))

def safe_response(query: str, context: str) -> dict:
    """Antwort mit Halluzinations-Risiko-Einschätzung."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
             "Antworte basierend auf dem gegebenen Kontext. "
             "Wenn du unsicher bist, sage 'Ich weiss es nicht'."},
            {"role": "user", "content":
             f"Kontext: {context}\n\nFrage: {query}"},
        ],
        temperature=0.0,
        logprobs=True,
        top_logprobs=5,
    )

    answer = response.choices[0].message.content
    risk = estimate_hallucination_risk(response)

    if risk > 0.7:
        return {
            "answer": "Ich bin mir bei dieser Antwort unsicher. "
                      "Bitte überprüfe die Informationen.",
            "risk": risk,
            "original_answer": answer,
        }

    return {"answer": answer, "risk": risk}

# Beispiel
result = safe_response(
    "Wie hoch war der Umsatz?",
    "Der Umsatz betrug 42 Millionen Euro."
)
print(f"Antwort: {result['answer']}")
print(f"Risiko: {result['risk']:.2%}")

