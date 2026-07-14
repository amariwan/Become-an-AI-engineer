# Token-Budget-System
# Quelle: chapters/06_token_verwaltung.tex (Zeile 555)
class TokenBudget:
    def __init__(self, max_input: int, max_output: int):
        self.max_input = max_input
        self.max_output = max_output

    def check(self, input_tokens: int, output_tokens: int) -> bool:
        return (input_tokens <= self.max_input and
                output_tokens <= self.max_output)

    def truncate_input(self, text: str, encoding) -> str:
        tokens = encoding.encode(text)
        if len(tokens) <= self.max_input:
            return text
        return encoding.decode(tokens[:self.max_input])

# Nutzung
budget = TokenBudget(max_input=4096, max_output=512)

if not budget.check(input_tokens, request_max):
    print(f"Input {input_tokens} ueberschreitet Budget {budget.max_input}")
    text = budget.truncate_input(text, encoding)

