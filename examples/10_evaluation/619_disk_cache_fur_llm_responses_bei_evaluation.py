# Disk-Cache für LLM-Responses bei Evaluation
# Quelle: chapters/10_evaluation.tex (Zeile 619)
import json
import hashlib
from pathlib import Path

class EvalCache:
    """Persistenter Cache für LLM-Responses in der Evaluation."""

    def __init__(self, cache_dir: str = ".eval_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _key(self, prompt: str, model: str) -> str:
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> str | None:
        key = self._key(prompt, model)
        path = self.cache_dir / f"{key}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    def set(self, prompt: str, model: str, response: str):
        key = self._key(prompt, model)
        path = self.cache_dir / f"{key}.json"
        path.write_text(json.dumps(response))

cache = EvalCache()

def cached_eval(example: dict) -> dict:
    """Mit Cache, um wiederholte API-Calls zu vermeiden."""
    cached = cache.get(example["input"], "gpt-4o-mini")
    if cached:
        return {"input": example["input"], "cached": True, **cached}

    response = call_llm("gpt-4o-mini", example["input"])
    cache.set(example["input"], "gpt-4o-mini", response)
    return {"input": example["input"], "cached": False, "response": response}

