# QLoRA -- Fine-Tuning eines quantisierten Modells
# Quelle: chapters/18_modellanpassung.tex (Zeile 173)
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.3-70B-Instruct",
    quantization_config=bnb_config,
    device_map="auto",
)

model = get_peft_model(model, lora_config)
# Modell in 4-Bit geladen (~35 GB VRAM fuer 70B)
# LoRA-Adapter in BF16 trainiert (~8 MB zusaetzlich)

