# Semantic Router mit Intent-Klassifikation
# Quelle: chapters/19_caching_routing_guardrails.tex (Zeile 273)
from enum import Enum

class Intent(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
    CODE = "code"
    REFUSAL = "refusal"  # Unerlaubte Anfragen

class SemanticRouter:
    def __init__(self):
        self.routes = {
            Intent.SIMPLE: {
                "model": "gpt-4o-mini",
                "max_tokens": 256,
                "cost_per_call": 0.0001,
            },
            Intent.COMPLEX: {
                "model": "claude-sonnet-4",
                "max_tokens": 2048,
                "cost_per_call": 0.003,
            },
            Intent.CODE: {
                "model": "codestral-latest",
                "max_tokens": 1024,
                "cost_per_call": 0.002,
            },
        }
        self.classifier_model = "gpt-4o-mini"

    def classify(self, query: str) -> Intent:
        prompt = (
            "Klassifiziere die folgende Anfrage in eine Kategorie.\n"
            f"- '{Intent.SIMPLE.value}': Einfache Frage, "
            f"z.B. Status, Datum, Faktenabfrage\n"
            f"- '{Intent.COMPLEX.value}': Komplexe Analyse, "
            "mehrschrittiges Reasoning, Vergleich\n"
            f"- '{Intent.CODE.value}': Code-Generierung, "
            "Debugging, SQL, Regex\n"
            f"- '{Intent.REFUSAL.value}': Illegal, gefaehrlich, "
            "personenbezogene Daten, Passwoerter\n"
            f"\nAnfrage: {query}\n"
            f"Antwort NUR mit dem Kategorie-String."
        )
        response = call_llm(self.classifier_model, prompt,
                            temperature=0.0)
        try:
            return Intent(response.strip().lower())
        except ValueError:
            return Intent.SIMPLE

    def route(self, query: str, user_id: str = None) -> dict:
        intent = self.classify(query)

        if intent == Intent.REFUSAL:
            return {
                "intent": intent.value,
                "response": "Diese Anfrage kann nicht "
                           "bearbeitet werden.",
                "cost": 0.0,
            }

        route = self.routes.get(intent, self.routes[Intent.SIMPLE])

        cached_response = semantic_cache.lookup(query)
        if cached_response[0]:
            return {
                "intent": intent.value,
                "response": cached_response[0],
                "cost": 0.0,
                "cached": True,
            }

        response = call_llm(
            route["model"],
            query,
            max_tokens=route["max_tokens"],
        )

        return {
            "intent": intent.value,
            "model": route["model"],
            "response": response,
            "cost": route["cost_per_call"],
            "cached": False,
        }

router = SemanticRouter()
result = router.route("Was ist der Status meiner Bestellung #12345?")
print(f"Intent: {result['intent']}, "
      f"Modell: {result.get('model', 'blocked')}, "
      f"Cost: EUR{result['cost']:.4f}")

