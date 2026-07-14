# Few-Shot Prompting
# Quelle: chapters/07_prompt_design.tex (Zeile 213)
FEW_SHOT = [
    {"input": "Ich habe das falsche Produkt erhalten.",
     "output": '{"priority": 3, "category": "complaint", "urgency": "medium"}'},
    {"input": "Die Rechnung zeigt einen falschen Betrag.",
     "output": '{"priority": 4, "category": "billing", "urgency": "high"}'},
    {"input": "Wuerdet ihr bald Widget X anbieten?",
     "output": '{"priority": 1, "category": "feature_request", "urgency": "low"}'},
]

def build_few_shot_prompt(examples: list[dict], user_input: str) -> str:
    prompt_parts = [
        "Klassifiziere das Ticket als JSON mit priority, category, urgency.",
        *[f"Input: {e['input']}\nOutput: {e['output']}"
          for e in examples],
        f"Input: {user_input}\nOutput:",
    ]
    return "\n\n".join(prompt_parts)

