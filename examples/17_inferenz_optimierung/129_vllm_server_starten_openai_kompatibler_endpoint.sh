# vLLM-Server starten (OpenAI-kompatibler Endpoint)
# Quelle: chapters/17_inferenz_optimierung.tex (Zeile 129)
# Installation
pip install vllm

# Llama 3 70B auf 4 GPUs starten
vllm serve meta-llama/Llama-3.3-70B-Instruct \
    --tensor-parallel-size 4 \
    --dtype auto \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.90 \
    --max-num-seqs 32 \
    --enable-prefix-caching

# Client-Code (OpenAI-kompatibel)
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": "Erklaere PagedAttention."}],
    max_tokens=512,
    temperature=0.1,
)
print(response.choices[0].message.content)

