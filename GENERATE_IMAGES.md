# gemini-create-photo Batch Generation Script

## Verwendung

```bash
# Einzelnes Bild generieren
gemini-create-photo --prompt "$(cat images/07_rag/fig01_rag_pipeline_overview.prompt)" \
  --output images/07_rag/fig01_rag_pipeline_overview.png

# Oder mit JSON Manifest
python3 generate_all.py
```

## generate_all.py

```python
#!/usr/bin/env python3
import json
import subprocess
import os

with open('images_manifest.json') as f:
    manifest = json.load(f)

for img in manifest['images']:
    out_path = img['file']
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    if os.path.exists(out_path):
        print(f"SKIP: {out_path} exists")
        continue
    
    print(f"Generating: {out_path}")
    result = subprocess.run([
        'gemini-create-photo',
        '--prompt', img['prompt'],
        '--output', out_path
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
    else:
        print(f"OK: {out_path}")

print("Done!")
```

## Ordner-Struktur erstellen

```bash
mkdir -p images/07_rag images/08_agents images/11_inference_opt \
         images/01_rolle images/03_landschaft images/04_openai_api \
         images/05_token images/06_prompt
```

## LaTeX Einbindung (in Kapiteln)

Nach Generation in jeweiliges Kapitel einfügen:

```latex
% Kapitel 07 - nach Zeile 62
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{images/07_rag/fig01_rag_pipeline_overview.pdf}
  \caption{RAG-System: Offline Indexing Pipeline (links) und Online Runtime Pipeline (rechts)}
  \label{fig:rag-pipeline-overview}
\end{figure}
```

## Format Hinweise

- **PNG** für Screenshots/UI-Mockups
- **PDF/SVG** für Diagramme (skalierbar, LaTeX-nativ)
- **gemini-create-photo** liefert PNG - für PDF in LaTeX konvertieren:
  ```bash
  convert fig01.png fig01.pdf  # ImageMagick
  # oder
  inkscape fig01.png -o fig01.pdf
  ```

## Priorität-Reihenfolge

1. **07_rag** (7 Bilder) - Kernkapitel, komplexeste Pipeline
2. **08_agents** (11 Bilder) - Viele Architektur-Diagramme
3. **11_inference_opt** (8 Bilder) - Technische Visualisierungen
4. **01_rolle, 03_landschaft, 04_openai_api, 05_token, 06_prompt** - Einstiegs-Kapitel
5. **09_eval, 10_deployment, 12_caching, 13_finetuning, 14_multimodal, 15_mlops, 16_security, appendix** - Später