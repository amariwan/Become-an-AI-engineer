# Multi-LoRA-Serving mit vLLM
# Quelle: chapters/18_modellanpassung.tex (Zeile 417)
# Server starten mit mehreren LoRA-Adaptern
vllm serve meta-llama/Llama-3.3-70B-Instruct \
    --lora-modules sql=/path/to/lora-sql \
    --lora-modules email=/path/to/lora-email \
    --lora-modules code=/path/to/lora-code \
    --max-lora-rank 32 \
    --enable-lora

# Client: Adapter per Header waehlen
response = client.chat.completions.create(
    model="sql",  # LoRA-Adapter-Name
    messages=[{"role": "user", "content": "SELECT * FROM users..."}],
    extra_body={"max_tokens": 256},
)

