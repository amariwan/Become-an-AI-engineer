# Response-Caching mit Disk-Cache
# Quelle: chapters/06_token_verwaltung.tex (Zeile 630)
import hashlib
import json
import os

class ResponseCache:
    def __init__(self, cache_dir: str = ".token_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _key(self, messages: list[dict], model: str) -> str:
        raw = json.dumps({"messages": messages, "model": model},
                         sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, messages, model):
        key = self._key(messages, model)
        path = f"{self.cache_dir}/{key}.json"
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return None

    def set(self, messages, model, response):
        key = self._key(messages, model)
        with open(f"{self.cache_dir}/{key}.json", "w") as f:
            json.dump(response, f)

