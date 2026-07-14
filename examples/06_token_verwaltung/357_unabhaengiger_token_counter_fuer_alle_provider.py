# Unabhaengiger Token-Counter fuer alle Provider
# Quelle: chapters/06_token_verwaltung.tex (Zeile 357)
class TokenCounter:
    def __init__(self):
        self._openai_encoding = tiktoken.get_encoding("o200k_base")

    def count_openai(self, text: str) -> int:
        return len(self._openai_encoding.encode(text))

    def count_anthropic(self, text: str) -> int:
        from anthropic import Anthropic
        return Anthropic().count_tokens(text)

    def count_gemini(self, text: str, model_name: str = "gemini-2.0-flash") -> int:
        import google.generativeai as genai
        model = genai.GenerativeModel(model_name)
        return model.count_tokens(text).total_tokens

    def count_llama(self, text: str) -> int:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def estimate_cost(self, provider: str, model: str,
                      input_tokens: int, output_tokens: int) -> float:
        prices = {
            ("openai", "gpt-4o"):       (2.50, 10.00),
            ("openai", "gpt-4o-mini"):  (0.15, 0.60),
            ("anthropic", "claude-4"):  (3.00, 15.00),
            ("google", "gemini-2.0"):   (1.00, 4.00),
        }
        input_price, output_price = prices.get(
            (provider, model), (0.0, 0.0)
        )
        return (input_tokens / 1_000_000 * input_price +
                output_tokens / 1_000_000 * output_price)

