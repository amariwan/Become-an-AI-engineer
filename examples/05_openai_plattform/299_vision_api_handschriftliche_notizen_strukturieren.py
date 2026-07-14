# Vision API: Handschriftliche Notizen strukturieren
# Quelle: chapters/05_openai_plattform.tex (Zeile 299)
import base64

with open("notiz.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system",
         "content": "Extrahiere Medikation, Dosierung und Datum aus dem Bild."},
        {"role": "user",
         "content": [
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
            {"type": "text",
             "text": "Strukturiere die Informationen als JSON."}
        ]}
    ],
    response_format={"type": "json_object"},
)

