# Response Cache mit Hash-Key
# Quelle: chapters/19_caching_routing_guardrails.tex (Zeile 97)
import hashlib
import json
from diskcache import Cache  # pip install diskcache

class ResponseCache:
    def __init__(self, cache_dir: str = ".llm_cache",
                 ttl: int = 3600):
        self.cache = Cache(cache_dir)
        self.ttl = ttl

    def _key(self, messages: list[dict], model: str) -> str:
        content = json.dumps(messages, sort_keys=True) + model
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, messages: list[dict], model: str) -> str | None:
        key = self._key(messages, model)
        return self.cache.get(key)

    def set(self, messages: list[dict], model: str, response: str):
        key = self._key(messages, model)
        self.cache.set(key, response, expire=self.ttl)

    def get_or_call(self, messages, model, llm_func):
        cached = self.get(messages, model)
        if cached:
            return cached, True  # Hit
        response = llm_func(messages, model)
        self.set(messages, model, response)
        return response, False  # Miss

