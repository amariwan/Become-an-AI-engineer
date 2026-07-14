# Plan-and-Solve Agent
# Quelle: chapters/09_ai_agenten.tex (Zeile 633)
class PlanAndSolveAgent:
    def run(self, task: str) -> str:
        # Phase 1: Plan erstellen
        plan_response = self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": (
                f"Erstelle einen detaillierten Plan fuer diese Aufgabe. "
                f"Liste die Schritte 1..N auf:\n{task}"
            )}],
        )
        plan = plan_response.choices[0].message.content
        steps = self._parse_steps(plan)

        # Phase 2: Schritte ausfuehren
        results = []
        for step in steps:
            result = self._execute_step(step)
            results.append(result)

        # Phase 3: Zusammenfassen
        return self._synthesize(task, results)

    def _parse_steps(self, plan: str) -> list[str]:
        return [line.strip() for line in plan.split("\n")
                if line.strip().startswith(("1.", "2.", "3.", "4.", "5."))]

