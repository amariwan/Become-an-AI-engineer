# Supervisor + Worker Pattern
# Quelle: chapters/09_ai_agenten.tex (Zeile 665)
class SupervisorAgent:
    def __init__(self):
        self.workers = {
            "researcher": ResearcherAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
        }

    def run(self, task: str) -> str:
        # Schritt 1: Entscheiden, welche Worker gebraucht werden
        plan = self._plan(task)
        results = {}

        # Schritt 2: Worker in der richtigen Reihenfolge ausfuehren
        for worker_name in plan["worker_sequence"]:
            worker = self.workers[worker_name]
            results[worker_name] = worker.run(
                task=plan["tasks"][worker_name],
                context=results,
            )

        # Schritt 3: Ergebnisse zusammenfuehren
        return self._synthesize(results)

