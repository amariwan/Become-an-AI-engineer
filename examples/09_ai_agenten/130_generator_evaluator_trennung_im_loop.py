# Generator-Evaluator-Trennung im Loop
# Quelle: chapters/09_ai_agenten.tex (Zeile 130)
class LoopEngine:
    """Trennt Erzeugung und Bewertung in zwei unabhaengige Phasen."""

    def __init__(self, generator, evaluator, max_iterations: int = 5):
        self.generator = generator
        self.evaluator = evaluator
        self.max_iterations = max_iterations
        self.memory = LoopMemory()

    def run(self, task: str) -> str:
        for iteration in range(1, self.max_iterations + 1):
            # Phase 1: Erzeugen
            output = self.generator.generate(task, self.memory.context())
            self.memory.add_step("generate", task, output)

            # Phase 2: Bewerten (durch unabhaengige Instanz)
            eval_result = self.evaluator.evaluate(task, output)
            self.memory.add_step("evaluate", output, str(eval_result))

            if eval_result["passed"]:
                return output

            # Phase 3: Feedback einarbeiten
            task = f"{task}\n\nFeedback: {eval_result['feedback']}"

        raise RuntimeError(f"Nach {self.max_iterations} Iterationen kein Ergebnis.")

