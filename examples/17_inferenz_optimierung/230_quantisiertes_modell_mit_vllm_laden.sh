# Quantisiertes Modell mit vLLM laden
# Quelle: chapters/17_inferenz_optimierung.tex (Zeile 230)
vllm serve ./llama-70b-awq \
    --quantization awq \
    --tensor-parallel-size 2  # Jetzt auf 2 GPUs statt 4

