# Chat-History mit automatischer Kompression
# Quelle: chapters/06_token_verwaltung.tex (Zeile 458)
from collections import deque
import tiktoken

class ConversationMemory:
    def __init__(self, model: str = "gpt-4o", max_tokens: int = 120_000):
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        self.max_tokens = max_tokens
        self.history: deque[dict] = deque()
        self.system_prompt: str = ""

    def add_message(self, role: str, content: str):
        if role == "system":
            self.system_prompt = content
            return
        self.history.append({"role": role, "content": content})
        if self._current_tokens() > self.max_tokens * 0.8:
            self._compress()

    def _current_tokens(self) -> int:
        total = len(self.encoding.encode(self.system_prompt))
        for msg in self.history:
            total += 3 + len(self.encoding.encode(msg["content"]))
        return total

    def _compress(self):
        if len(self.history) < 4:
            return
        recent = list(self.history)[-2:]
        old = list(self.history)[:-2]
        summary = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": "Fasse diese Chat-Nachrichten in einem Satz"
                           " zusammen: " + " ".join(
                               m["content"] for m in old
                           )
            }],
            max_tokens=100,
        ).choices[0].message.content
        self.history = deque(
            [{"role": "user", "content": f"[Summary: {summary}]"}]
            + recent
        )

    def get_messages(self) -> list[dict]:
        msgs = [{"role": "system", "content": self.system_prompt}]
        msgs.extend(self.history)
        return msgs

