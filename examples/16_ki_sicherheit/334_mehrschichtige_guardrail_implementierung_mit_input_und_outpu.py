# Mehrschichtige Guardrail-Implementierung mit Input- und Output-Kontrolle
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 334)
import re
from typing import Optional

class PromptGuardrail:
    def __init__(self):
        self.blocked_input_patterns = [
            r"ignoriere.*anweisungen?",
            r"ignore.*(instructions|previous)",
            r"system.*prompt",
            r"dAN|assistant.*ohne.*einschränkung",
        ]
        self.blocked_output_patterns = [
            r"api.?key",
            r"passwort|password",
            r"zugangsdaten|credentials",
            r"\b[A-Za-z0-9]{20,}\b",  # potenzielle Tokens
        ]

    def check_input(self, text: str) -> bool:
        """Prueft Eingabe auf verdaechtige Muster. Gibt True zurueck, wenn sie sicher ist."""
        for pattern in self.blocked_input_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                print(f"INPUT-BLOCK: Muster '{pattern}' erkannt")
                return False
        return True

    def sanitize_output(self, text: str) -> Optional[str]:
        """Filtert sensible Daten aus der Ausgabe."""
        for pattern in self.blocked_output_patterns:
            text = re.sub(pattern, "[REDAKTION]", text, flags=re.IGNORECASE)
        return text

    def process(self, user_input: str, model_response: str) -> Optional[str]:
        if not self.check_input(user_input):
            return "Ihre Anfrage konnte nicht verarbeitet werden."
        return self.sanitize_output(model_response)

guardrail = PromptGuardrail()
safe = guardrail.process(
    "Wie lautet der API-Key?",
    "Der API-Key lautet sk-abc123def456."
)
print(safe)  # "Der [REDAKTION] lautet [REDAKTION]."

