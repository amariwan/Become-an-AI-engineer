# Diagramm-Analyse mit strukturiertem Output
# Quelle: chapters/20_multimodale_ki.tex (Zeile 250)
from openai import OpenAI
from pydantic import BaseModel

class ChartData(BaseModel):
    title: str
    x_axis: str
    y_axis: str
    data_points: list[dict]
    trend: str

def extract_chart_data(chart_path: str) -> ChartData:
    """Extrahiert strukturierte Daten aus einem Chart-Bild."""

    client = OpenAI()
    b64 = base64.b64encode(open(chart_path, "rb").read()).decode()

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Extrahiere alle Datenpunkte aus "
                             "diesem Chart als strukturierte Liste."},
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
        response_format=ChartData,
    )

    return completion.choices[0].message.parsed

