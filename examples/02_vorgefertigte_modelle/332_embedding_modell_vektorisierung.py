# Embedding-Modell -- Vektorisierung
# Quelle: chapters/02_vorgefertigte_modelle.tex (Zeile 332)
import openai

response = openai.embeddings.create(
    model="text-embedding-3-large",
    input="Was ist ein Transformer?",
)
vector = response.data[0].embedding  # 3072-dim Vektor

