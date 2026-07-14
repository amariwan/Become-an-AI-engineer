# Model-Stealing-Detection: Ungewöhnliche API-Zugriffsmuster erkennen
# Quelle: chapters/16_ki_sicherheit.tex (Zeile 881)
from collections import defaultdict
from datetime import datetime, timedelta
import numpy as np

class StealingDetector:
    def __init__(self, threshold_embeddings: int = 1000):
        self.client_queries = defaultdict(list)
        self.threshold = threshold_embeddings

    def log_query(self, client_id: str, prompt: str,
                  response_len: int):
        self.client_queries[client_id].append({
            "timestamp": datetime.now(),
            "prompt": prompt,
            "response_len": response_len,
        })
        self._check_anomaly(client_id)

    def _check_anomaly(self, client_id: str):
        queries = self.client_queries[client_id]
        window = datetime.now() - timedelta(hours=1)
        recent = [q for q in queries if q["timestamp"] > window]

        # Kennzahl 1: Abfragevolumen
        if len(recent) > self.threshold:
            print(f"ALARM: Client {client_id[:8]} "
                  f"sandte {len(recent)} Anfragen in einer Stunde")

        # Kennzahl 2: Aehnlichkeit der Prompts
        if len(recent) >= 5:
            lengths = [len(q["prompt"]) for q in recent]
            variance = np.std(lengths) if len(lengths) > 1 else 0
            if variance < 5:
                print(f"ALARM: Client {client_id[:8]} "
                      f"sendet fast identische Prompt-Laengen "
                      f"(Std: {variance:.1f}) -- systematische Abfrage")

    def generate_report(self, client_id: str) -> dict:
        queries = self.client_queries.get(client_id, [])
        return {
            "client": client_id,
            "total_queries": len(queries),
            "time_span": "unknown",
            "stealing_risk": "HOCH" if len(queries) > 5000 else "NIEDRIG"
        }

detector = StealingDetector()
for i in range(1500):
    detector.log_query("attacker-123", "What is ...", 200)
print(detector.generate_report("attacker-123"))

