# Multimodale Image-Input-Pipeline
# Quelle: chapters/20_multimodale_ki.tex (Zeile 114)
from openai import OpenAI
import base64
from pathlib import Path

class MultimodalPipeline:
    """Verarbeitet Bilder, PDFs und Diagramme via LLM Vision."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def encode_image(self, image_path: str) -> str:
        """Bild in Base64 kodieren fuer den API-Call."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """Bild mit Prompt analysieren."""
        b64 = self.encode_image(image_path)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{b64}",
                                "detail": "high",
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content

