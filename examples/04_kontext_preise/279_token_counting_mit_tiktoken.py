# Token-Counting mit tiktoken
# Quelle: chapters/04_kontext_preise.tex (Zeile 279)
import tiktoken

def count_tokens(text: str,
                 model: str = "gpt-4o") -> int:
    """Zahle die Tokens eines Textes fur ein bestimmtes Modell."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def enforce_context_budget(
    messages: list[dict],
    max_tokens: int = 100_000,
    model: str = "gpt-4o",
) -> list[dict]:
    """Stelle sicher, dass der Prompt ins Context-Window passt."""
    total = 0
    budget_messages = []

    for msg in reversed(messages):
        tokens = count_tokens(msg["content"], model)
        if total + tokens > max_tokens:
            break
        budget_messages.insert(0, msg)
        total += tokens

    return budget_messages

# Beispiel: Chat-History managen
history = [
    {"role": "user", "content": "Frage 1"},
    {"role": "assistant", "content": "Antwort 1"},
    # ... viele weitere Nachrichten
    {"role": "user", "content": "Frage 50"},
]

budget = enforce_context_budget(
    history, max_tokens=50_000
)
print(f"Gekurzt von {len(history)} auf {len(budget)} Nachrichten")

