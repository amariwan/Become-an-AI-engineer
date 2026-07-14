# Supervisor-Worker-Architektur
# Quelle: chapters/09_ai_agenten.tex (Zeile 809)
class SupervisorAgent:
    """Koordiniert spezialisierte Worker-Agenten."""

    def __init__(self, workers: dict[str, callable]):
        self.workers = workers
        self.llm = get_llm()

    async def run(self, task: str) -> dict:
        plan = await self.llm.complete(
            f"Analysiere die Aufgabe und erstelle einen Plan "
            f"mit Workern: {list(self.workers.keys())}."
            f"\nAufgabe: {task}"
        )
        results = {}
        for step in self._parse_steps(plan):
            w = step["worker"]
            results[w] = await self.workers[w](step["task"])

        synthesis = await self.llm.complete(
            f"Synthetisiere Ergebnisse zu einer Antwort:\n"
            f"{json.dumps(results, indent=2)}"
        )
        return {"plan": plan, "results": results, "answer": synthesis}

    def _parse_steps(self, plan: str) -> list[dict]:
        steps = []
        for line in plan.split("\n"):
            if "->" in line and ":" in line:
                worker, task = line.split(":", 1)
                steps.append({
                    "worker": worker.strip().split("->")[-1].strip(),
                    "task": task.strip(),
                })
        return steps

