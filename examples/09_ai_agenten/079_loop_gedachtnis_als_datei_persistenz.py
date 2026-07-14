# Loop-Gedächtnis als Datei-Persistenz
# Quelle: chapters/09_ai_agenten.tex (Zeile 79)
class LoopMemory:
    """Ein strukturell einfaches, aber wirkungsvolles Gedaechtnis."""
    def __init__(self, path: str = "loop_state.json"):
        self.path = path
        self.history: list[dict] = []
        self._load()

    def _load(self):
        try:
            with open(self.path) as f:
                data = json.load(f)
                self.history = data.get("history", [])
        except FileNotFoundError:
            self.history = []

    def save(self):
        with open(self.path, "w") as f:
            json.dump({"history": self.history[-100:]}, f)

    def add_step(self, step_type: str, content: str, result: str):
        self.history.append({
            "step": len(self.history) + 1,
            "type": step_type,
            "content": content,
            "result": result,
            "timestamp": time.time(),
        })
        self.save()

    def context(self, last_n: int = 5) -> str:
        recent = self.history[-last_n:]
        return "\n".join(
            f"#{s['step']} [{s['type']}]: {s['content']} -> {s['result'][:200]}"
            for s in recent
        )

