# Bias-Erkennung: Automatische Detection von Stereotypen
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 201)
def detect_bias(text: str) -> dict:
    """Erkennt potenzielle Bias-Muster in einer LLM-Antwort."""

    gender_cues = {
        "typical_male": ["Der Arzt sagte", "Er als Manager"],
        "typical_female": ["Die Pflegekraft meinte", "Sie als Sekretarin"],
    }

    detected = {}
    for bias_type, cues in gender_cues.items():
        for cue in cues:
            if cue.lower() in text.lower():
                detected[bias_type] = detected.get(bias_type, 0) + 1

    return {
        "has_bias": len(detected) > 0,
        "bias_types": list(detected.keys()),
        "severity": "high" if len(detected) > 2 else "low",
    }

def safe_rag_query(query: str) -> str:
    """RAG-Query mit Bias-Detection."""
    answer = rag_chain.invoke(query)

    bias_check = detect_bias(answer)
    if bias_check["has_bias"]:
        validation = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"Ist diese Antwort gender-neutral "
                           f"und kulturell fair?\n\n{answer}"
            }],
        )
        if "ja" not in validation.choices[0].message.content.lower():
            answer = "Die Anfrage kann nicht neutral beantwortet werden."

    return answer

