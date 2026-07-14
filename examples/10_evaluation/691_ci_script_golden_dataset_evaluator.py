# CI-Script: Golden-Dataset-Evaluator
# Quelle: chapters/10_evaluation.tex (Zeile 691)
"""run_golden.py -- Fuhrt Golden-Dataset-Evaluation aus."""
import json
import sys
from pathlib import Path

def load_golden(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)

def evaluate_dataset(dataset: list[dict]) -> dict:
    results = []
    passed = 0
    for case in dataset:
        output = call_llm(case["prompt"])
        is_correct = judge_output(
            output, case["expected"], case["criteria"]
        )
        if is_correct:
            passed += 1
        results.append({
            "id": case["id"],
            "passed": is_correct,
            "latency_ms": output["latency_ms"],
            "cost": output["cost"],
        })

    pass_rate = passed / len(dataset)
    return {
        "pass_rate": pass_rate,
        "total": len(dataset),
        "passed": passed,
        "failed": len(dataset) - passed,
        "results": results,
    }

def check_threshold(report: dict,
                    threshold: float = 0.85) -> bool:
    """Exit 1 wenn Pass-Rate unter Threshold."""
    if report["pass_rate"] < threshold:
        print(f"FAIL: {report['pass_rate']:.1%} < {threshold:.0%}")
        sys.exit(1)
    print(f"PASS: {report['pass_rate']:.1%}")
    return True

if __name__ == "__main__":
    dataset = load_golden(sys.argv[1])
    report = evaluate_dataset(dataset)
    check_threshold(report)

