# Anthropic Token-Counting (Claude)
# Quelle: chapters/06_token_verwaltung.tex (Zeile 328)
# Anthropic: count_tokens ist im SDK enthalten
from anthropic import Anthropic

client = Anthropic()
token_count = client.count_tokens(
    "Das ist ein Test-Prompt fuer Claude."
)
print(f"Claude Tokens: {token_count}")

# Oder manuell mit anthropic-tokenizer
from anthropic_tokenizer import count_tokens as claude_count

tokens = claude_count("Dein Prompt hier")

