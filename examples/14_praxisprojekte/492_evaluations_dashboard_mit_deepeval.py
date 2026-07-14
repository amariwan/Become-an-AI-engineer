# Evaluations-Dashboard mit DeepEval
# Quelle: chapters/14_praxisprojekte.tex (Zeile 492)
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
    GEval
)
from deepeval.dataset import GoldenDataset

# Golden Dataset definieren
dataset = GoldenDataset(
    name="customer-support",
    test_cases=[
        LLMTestCase(
            input="Wie lautet eure Rueckgabepolitik?",
            actual_output="Sie haben 30 Tage Rueckgaberecht.",
            expected_output="30 Tage Rueckgaberecht, kostenlos",
            context=["Rueckgabepolitik: 30 Tage, kostenlos"]
        ),
    ]
)

# Metriken definieren
metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.8),
    HallucinationMetric(threshold=0.3),
    GEval(
        name="Professionalism",
        criteria="Bewerte die Professionalitaet der Antwort",
        evaluation_steps=[
            "Ist die Antwort hoeflich?",
            "Ist die Antwort vollstaendig?",
            "Enthaelt sie Quellenangaben?"
        ]
    )
]

# Evaluierung laufen lassen
results = evaluate(
    test_cases=dataset.test_cases,
    metrics=metrics,
    run_async=False
)

# Report generieren
for test_case in results.test_cases:
    print(f"\nInput: {test_case.input[:40]}...")
    for metric in test_case.metrics:
        status = "BESTANDEN" if metric.success else "FAILED"
        print(f"  [{status}] {metric.__name__}: "
              f"{metric.score:.2f}")

