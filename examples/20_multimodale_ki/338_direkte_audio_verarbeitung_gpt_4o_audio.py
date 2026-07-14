# Direkte Audio-Verarbeitung (GPT-4o-Audio)
# Quelle: chapters/20_multimodale_ki.tex (Zeile 338)
from openai import OpenAI


class AudioPipeline:
    """Verarbeitet Audio direkt ohne STT-Zwischenschritt."""

    def __init__(self):
        self.client = OpenAI()

    def analyze_audio(self, audio_path: str, prompt: str) -> str:
        """Audio-Inhalt mit Prompt analysieren."""
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        response = self.client.chat.completions.create(
            model="gpt-4o-audio-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": b64,
                                "format": "wav",
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    def extract_sentiment(self, audio_path: str) -> dict:
        """Stimmung und Sprechermerkmale extrahieren."""
        result = self.analyze_audio(
            audio_path,
            "Analysiere diese Audioaufnahme. "
            "Gib zurueck: Stimmung (positiv/neutral/negativ), "
            "Sprecheranzahl, Hintergrundgeraeusche, "
            "Sprechtempo (woerter/min), Pausen (Anzahl)."
        )
        return result

