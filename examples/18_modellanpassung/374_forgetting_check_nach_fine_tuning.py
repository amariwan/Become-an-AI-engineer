# Forgetting-Check nach Fine-Tuning
# Quelle: chapters/18_modellanpassung.tex (Zeile 374)
BENCHMARK = [
    {"input": "Was ist die Hauptstadt von Frankreich?",
     "expected": "Paris"},
    {"input": "Berechne 25 * 4 + 100",
     "expected": "200"},
    {"input": "Erklaere den Begriff 'RAG' in einem Satz.",
     "expected_contains": ["Retrieval", "Augmented", "Generation"]},
]

def evaluate_forgetting(model, tokenizer, benchmark):
    before_scores = run_benchmark("baseline_model", benchmark)
    after_scores = run_benchmark(model, benchmark)

    for task, before, after in zip(benchmark, before_scores, after_scores):
        diff = after - before
        status = "OK" if diff >= -0.05 else "FORGETTING"
        print(f"{status}: {task['input'][:40]}... "
              f"{before:.0%} -> {after:.0%} ({diff:+.0%})")

    # Gesamtdrift
    avg_drift = sum(
        a - b for a, b in zip(after_scores, before_scores)
    ) / len(benchmark)
    print(f"\nDurchschnittlicher Drift: {avg_drift:+.0%}")

    if avg_drift < -0.10:
        print("WARN: Staerker Drift! Dataset hat Allgemeinwissen beschaedigt.")
    elif avg_drift < -0.05:
        print("HINWEIS: Leichter Drift erkennbar. LoRA-Rang oder "
              "Lernrate pruefen.")
    else:
        print("OK: Kein signifikanter Knowledge-Drift.")

