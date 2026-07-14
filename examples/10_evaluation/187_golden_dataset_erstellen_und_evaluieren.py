# Golden Dataset erstellen und evaluieren
# Quelle: chapters/10_evaluation.tex (Zeile 187)
# 1. Golden Dataset definieren (manuell oder halbautomatisch)
GOLDEN_DATASET = [
    {
        "input": "Was ist eure Rueckgabepolitik?",
        "expected_output_type": "contains",
        "expected_keywords": ["30 Tage", "Kostenlos"],
        "should_not_contain": ["keine", "nicht moeglich"],
    },
    {
        "input": "Wie kann ich mein Abo kuendigen?",
        "expected_output_type": "json_schema",
        "expected_schema": {"cancellation_url": str, "deadline_days": int},
    },
    # 100+ mehr Beispiele fuer robuste Evaluation
]

# 2. Evaluations-Funktion schreiben
from typing import TypedDict

class EvalResult(TypedDict):
    input: str
    actual_output: str
    passed: bool
    score: float
    failures: list[str]

def evaluate_prompt(dataset: list[dict], prompt_fn) -> list[EvalResult]:
    """Evaluat den Prompt gegen das gesamte Golden Dataset."""
    results = []

    for example in dataset:
        actual_output = prompt_fn(example["input"])

        # Typ-basierte Validierung
        if example["expected_output_type"] == "contains":
            passed = all(
                kw in actual_output.lower()
                for kw in example["expected_keywords"]
            ) and not any(
                bad in actual_output.lower()
                for bad in example.get("should_not_contain", [])
            )
            score = sum(1 for kw in example["expected_keywords"] if kw in actual_output.lower()) / len(example["expected_keywords"])
        elif example["expected_output_type"] == "json_schema":
            try:
                parsed = json.loads(actual_output)
                passed = all(k in parsed for k in example["expected_schema"])
                score = sum(1 for k in example["expected_schema"] if k in parsed) / len(example["expected_schema"])
            except (json.JSONDecodeError, KeyError):
                passed, score = False, 0.0
        else:
            passed, score = False, 0.0

        results.append({
            "input": example["input"],
            "actual_output": actual_output[:200],
            "passed": passed,
            "score": score,
        })

    return results

# 3. Ausfuehren und Ergebnisse analysieren
results = evaluate_prompt(GOLDEN_DATASET, lambda x: call_llm(f"{SYSTEM_PROMPT}\n\n{x}"))
pass_rate = sum(1 for r in results if r["passed"]) / len(results) * 100
avg_score = sum(r["score"] for r in results) / len(results)

print(f"Pass Rate: {pass_rate:.1f}%")
print(f"Durchschnittliche Score: {avg_score:.2f}/1.0")

# Zeige die schwaechsten Beispiele zum Nachbessern
failed = [r for r in results if not r["passed"]]
for f in failed[:5]:
    print(f"\nFAILED: {f['input'][:40]}...")
    print(f"  Output: {f['actual_output'][:80]}...")

