# Speculative Decoding in vLLM
# Quelle: chapters/17_inferenz_optimierung.tex (Zeile 277)
vllm serve meta-llama/Llama-3.3-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5 \
    --tensor-parallel-size 4

