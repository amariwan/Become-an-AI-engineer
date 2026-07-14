# LLM Council mit anonymisierter Peer-Review
# Quelle: chapters/10_evaluation.tex (Zeile 385)
class LLMCouncil:
    """Multi-Perspektiven-Evaluation mit Peer-Review."""

    ADVISOR_ROLES = {
        "devils_advocate": (
            "Du hinterfragst Annahmen und suchst Schwachstellen. "
            "Gib 2-3 konkrete Kritikpunkte."
        ),
        "first_principles": (
            "Baue die Antwort von Grundprinzipien aus neu auf. "
            "Ignoriere bestehende Annahmen."
        ),
        "optimist": (
            "Du suchst Chancen und positive Aspekte. "
            "Wo liegen die groessten Potenziale?"
        ),
        "executor": (
            "Du bleibst bei der Umsetzung. "
            "Was sind die konkreten naechsten Schritte?"
        ),
        "outsider": (
            "Du hast kein Fachwissen in diesem Bereich. "
            "Ist die Analyse verstaendlich und plausibel?"
        ),
    }

    def evaluate(self, question: str) -> dict:
        # Phase 1: Jeder Advisor antwortet unabhaengig
        responses = {}
        for role, instruction in self.ADVISOR_ROLES.items():
            prompt = f"{instruction}\n\nFrage: {question}"
            responses[role] = call_llm("claude-sonnet-4", prompt)

        # Phase 2: Anonymisierte Peer-Review
        labels = list("ABCDE")
        anonymous = dict(zip(labels, responses.values()))
        reviews = {}

        for i, (role, label) in enumerate(zip(responses, labels)):
            peers = [l for j, l in enumerate(labels) if j != i]
            review_prompt = (
                f"Bewerte die folgenden fuenf Positionen anonym.\n"
                f"Deine eigene Position ist {label}.\n"
                f"Streiche die Position zusammen, "
                f"die die schwaechste Argumentation hat:\n"
            )
            for p_label in peers:
                review_prompt += (
                    f"\n--- Position {p_label} ---\n"
                    f"{anonymous[p_label][:500]}\n"
                )

            review_result = call_llm("gpt-4o", review_prompt,
                                     temperature=0.2)
            reviews[role] = review_result

        # Phase 3: Chairman synthetisiert
        chairman_prompt = (
            f"Du bist der Chairman eines AI Councils.\n\n"
            f"Frage: {question}\n\n"
            f"Analysen und Bewertungen:\n"
        )
        for role in responses:
            chairman_prompt += (
                f"\n--- {role} ---\n"
                f"Analyse: {responses[role][:300]}\n"
                f"Peer-Review: {reviews[role][:200]}\n"
            )
        chairman_prompt += (
            f"\nGib dein Urteil: "
            f"(1) Wo waren sich alle einig?\n"
            f"(2) Wo gab es Widersprueche?\n"
            f"(3) Was wurde uebersehen?\n"
            f"(4) Eine klare Handlungsempfehlung."
        )

        verdict = call_llm("claude-opus-4", chairman_prompt,
                           temperature=0.0)

        return {
            "question": question,
            "responses": responses,
            "reviews": reviews,
            "verdict": verdict,
        }

