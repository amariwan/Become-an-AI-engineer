# Multimodales Modell -- Bildanalyse
# Quelle: chapters/02_vorgefertigte_modelle.tex (Zeile 254)
import openai

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "Was steht auf diesem Schild?"},
            {"type": "image_url",
             "image_url": {"url": "https://example.com/schild.jpg"}}
        ]}
    ]
)

