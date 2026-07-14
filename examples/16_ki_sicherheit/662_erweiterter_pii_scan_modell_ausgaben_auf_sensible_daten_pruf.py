# Erweiterter PII-Scan: Modell-Ausgaben auf sensible Daten prüfen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 662)
import re

class PIIRedactor:
    patterns = {
        "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
        "phone": re.compile(r"\+?[\d\s\-/]{7,}"),
        "credit_card": re.compile(r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"),
        "api_key": re.compile(r"\b(sk|pk)_[a-zA-Z0-9]+\b"),
    }

    @classmethod
    def scan(cls, text: str) -> dict:
        findings = {}
        for name, pattern in cls.patterns.items():
            matches = pattern.findall(text)
            if matches:
                findings[name] = matches
        return findings

    @classmethod
    def redact(cls, text: str) -> str:
        for name, pattern in cls.patterns.items():
            text = pattern.sub(f"[{name.upper()}]", text)
        return text

response = "Meine Email ist max@beispiel.de und meine Karte 1234 5678 9012 3456."
result = PIIRedactor.scan(response)
print(f"Gefunden: {result}")
safe = PIIRedactor.redact(response)
print(f"Redigiert: {safe}")
# Ausgabe: Redigiert: Meine Email ist [EMAIL] und meine Karte [CREDIT_CARD].

