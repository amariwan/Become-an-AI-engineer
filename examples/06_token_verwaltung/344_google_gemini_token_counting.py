# Google Gemini Token-Counting
# Quelle: chapters/06_token_verwaltung.tex (Zeile 344)
# Google: Token-Counting ueber die API
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.count_tokens("Dein Prompt hier")
print(f"Gemini Tokens: {response.total_tokens}")

