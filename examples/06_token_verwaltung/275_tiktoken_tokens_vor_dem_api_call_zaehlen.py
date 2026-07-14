# TikToken: Tokens vor dem API-Call zaehlen
# Quelle: chapters/06_token_verwaltung.tex (Zeile 275)
import tiktoken

MODEL_ENCODINGS = {
    "gpt-4o": "o200k_base",
    "gpt-4o-mini": "o200k_base",
    "o1": "o200k_base",
    "o3": "o200k_base",
    "gpt-4": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
}

def get_encoding(model: str) -> tiktoken.Encoding:
    encoding_name = MODEL_ENCODINGS.get(model, "o200k_base")
    return tiktoken.get_encoding(encoding_name)

def count_tokens(messages: list[dict], model: str = "gpt-4o") -> int:
    encoding = get_encoding(model)
    tokens_per_message = 3
    tokens_per_name = 1

    total = 0
    for msg in messages:
        total += tokens_per_message
        for key, value in msg.items():
            if isinstance(value, str):
                total += len(encoding.encode(value))
            elif isinstance(value, list):
                for item in value:
                    if item.get("type") == "text":
                        total += len(encoding.encode(item["text"]))
                    elif item.get("type") == "image_url":
                        total += count_image_tokens(item["image_url"]["url"])
            if key == "name":
                total += tokens_per_name

    total += 3
    return total

def count_image_tokens(image_url: str, detail: str = "auto") -> int:
    if detail == "low":
        return 85
    if detail == "high":
        return 170  # 768x768 default
    if detail == "auto":
        return 85
    return 85

