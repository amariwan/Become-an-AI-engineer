# Supply-Chain-Incident-Response: Modell-Herkunft automatisiert prüfen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 559)
from datetime import datetime, timedelta

TRUSTED_SOURCES = {"trusted-model-repo", "internal-registry"}
BENCHMARK_HASHES = {
    "gpt-4o": "a1b2c3d4e5f6...",
    "llama-3": "6f5e4d3c2b1a...",
}

class SupplyChainMonitor:
    def __init__(self):
        self.deployment_log = []

    def check_deployment(self, metadata: dict) -> bool:
        issues = []

        source = metadata.get("source", "unknown")
        if source not in TRUSTED_SOURCES:
            issues.append(f"Unbekannte Quelle: {source}")

        model_hash = metadata.get("sha256", "")
        expected = BENCHMARK_HASHES.get(metadata.get("model_name", ""))
        if expected and model_hash != expected:
            issues.append(f"Pruefsummenabweichung fuer {metadata.get('model_name')}")

        if metadata.get("deploy_time", 0) > 60:
            issues.append(f"Ungewoehnlich langes Deployment: {metadata['deploy_time']}s")

        self.deployment_log.append({
            "timestamp": datetime.now(),
            "metadata": metadata,
            "issues": issues,
        })

        if issues:
            print("ALARM: Supply-Chain-Vorfall erkannt")
            for i in issues:
                print(f"  [!]  {i}")
            return False

        print("Deployment geprueft: OK")
        return True

monitor = SupplyChainMonitor()
monitor.check_deployment({
    "source": "trusted-model-repo",
    "model_name": "gpt-4o",
    "sha256": "a1b2c3d4e5f6...",
    "deploy_time": 45,
})

