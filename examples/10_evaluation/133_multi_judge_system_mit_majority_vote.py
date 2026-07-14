# Multi-Judge-System mit Majority-Vote
# Quelle: chapters/10_evaluation.tex (Zeile 133)
from collections import Counter

JUDGE_MODELS = ["gpt-4o", "claude-3.5-sonnet", "gemini-2.5-pro"]

def multi_judge(query: str, answer: str, rubric: str) -> dict:
    """Drei unabhängige Modelle bewerten, Majority-Vote als Ergebnis."""
    scores = []

    for model in JUDGE_MODELS:
        judge_prompt = (
            f"Bewerte die Antwort auf einer Skala 1-10.\n"
            f"Rubric: {rubric}\n"
            f"Frage: {query}\n"
            f"Antwort: {answer}\n"
            f"Gib NUR eine Zahl zurück."
        )
        response = call_llm(model, judge_prompt, temperature=0.0)
        try:
            scores.append(int(response.strip()))
        except ValueError:
            continue

    if not scores:
        return {"score": None, "confidence": 0.0}

    # Majority-Vote oder Median bei Streuung
    score_counts = Counter(scores)
    majority_score = score_counts.most_common(1)[0][0]

    return {
        "score": majority_score,
        "all_scores": scores,
        "agreement": max(score_counts.values()) / len(scores),
    }

result = multi_judge(
    query="Was ist der Unterschied zwischen RAG und Fine-Tuning?",
    answer="RAG ergänzt den Prompt mit relevanten Dokumenten, "
           "Fine-Tuning passt die Modellgewichte an.",
    rubric="Faktenrichtigkeit, Vollständigkeit, Klarheit"
)
print(f"Score: {result['score']}/10 | "
      f"Agreement: {result['agreement']:.0%}")
print(f"Einzelbewertungen: {result['all_scores']}")

