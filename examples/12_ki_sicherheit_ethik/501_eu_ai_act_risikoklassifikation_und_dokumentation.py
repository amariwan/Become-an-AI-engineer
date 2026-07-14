# EU-AI-Act-Risikoklassifikation und Dokumentation
# Quelle: chapters/12_ki_sicherheit_ethik.tex (Zeile 501)
from enum import Enum
from datetime import datetime

class RiskLevel(Enum):
    UNACCEPTABLE = "unacceptable"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"

class AISystemDocumentation:
    """Dokumentiert ein KI-System nach EU AI Act."""

    def __init__(self, name: str, version: str, purpose: str):
        self.name = name
        self.version = version
        self.purpose = purpose
        self.risk_level = RiskLevel.MINIMAL
        self.training_data: list[dict] = []
        self.performance_metrics: dict = {}
        self.human_oversight: bool = False
        self.created_at = datetime.now()

    def classify_risk(self) -> RiskLevel:
        """Automatische Risikoklassifikation nach EU AI Act Annex III."""
        high_risk_categories = [
            "biometric", "critical_infrastructure",
            "education", "employment", "credit",
            "law_enforcement", "migration", "justice",
        ]
        purpose_lower = self.purpose.lower()

        # Unacceptable Risk?
        unacceptable_keywords = [
            "social scoring", "real-time biometric",
            "predictive policing based on profiling",
        ]
        if any(k in purpose_lower for k in unacceptable_keywords):
            self.risk_level = RiskLevel.UNACCEPTABLE
            return self.risk_level

        # High Risk?
        if any(cat in purpose_lower
               for cat in high_risk_categories):
            self.risk_level = RiskLevel.HIGH
            return self.risk_level

        # Limited Risk (Transparenzpflicht)
        if not self.human_oversight:
            self.risk_level = RiskLevel.LIMITED
            return self.risk_level

        self.risk_level = RiskLevel.MINIMAL
        return self.risk_level

    def generate_report(self) -> dict:
        """Erzeugt den Compliance-Report fuer die Dokumentation."""
        return {
            "system_name": self.name,
            "version": self.version,
            "purpose": self.purpose,
            "risk_level": self.risk_level.value,
            "classification_date": self.created_at.isoformat(),
            "training_data": {
                "sources": len(self.training_data),
                "has_pii": any(
                    d.get("contains_pii", False)
                    for d in self.training_data
                ),
            },
            "performance": self.performance_metrics,
            "human_oversight": self.human_oversight,
            "conformity_assessment_required":
                self.risk_level == RiskLevel.HIGH,
        }

# Beispiel: Bewerbungs-Tool klassifizieren
doc = AISystemDocumentation(
    name="ResumeScorer",
    version="2.1.0",
    purpose="AI-powered resume screening for hiring managers",
)
doc.human_oversight = True
print(f"Risk level: {doc.classify_risk().value}")
# -> high
print(f"CE assessment needed: "
      f"{doc.generate_report()['conformity_assessment_required']}")
# -> True

