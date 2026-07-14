# Closed Source (OpenAI) vs. Open Source (Ollama) im Vergleich
# Quelle: chapters/02_vorgefertigte_modelle.tex (Zeile 639)
# === Variante A: Closed Source (OpenAI API) ===
import openai

def generate_product_description(product_name: str, features: list[str]) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "Du bist ein Marketing-Assistent."},
            {"role": "user",
             "content": f"Produkt: {product_name}\n"
                        f"Merkmale: {', '.join(features)}\n"
                        f"Schreibe eine ansprechende Beschreibung "
                        f"in 3-4 Satzen."}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# === Variante B: Open Source (Ollama lokal) ===
import requests

def generate_product_description_local(
    product_name: str, features: list[str]
) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": f"Produkt: {product_name}\n"
                      f"Merkmale: {', '.join(features)}\n"
                      f"Schreibe eine ansprechende Beschreibung "
                      f"in 3-4 Satzen.",
            "stream": False,
        },
    )
    return response.json()["response"]

