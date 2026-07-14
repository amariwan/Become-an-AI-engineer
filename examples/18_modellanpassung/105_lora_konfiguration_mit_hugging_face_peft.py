# LoRA-Konfiguration mit Hugging Face PEFT
# Quelle: chapters/18_modellanpassung.tex (Zeile 105)
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,                     # Rang der LoRA-Matrizen
    lora_alpha=32,            # Skalierungsfaktor (alpha / r)
    target_modules=[          # Welche Schichten erhalten LoRA?
        "q_proj",             # Query-Projektion
        "k_proj",             # Key-Projektion
        "v_proj",             # Value-Projektion
        "o_proj",             # Output-Projektion
    ],
    lora_dropout=0.05,        # Dropout für Regularisierung
    bias="none",              # Bias-Gewichte nicht trainieren
    task_type="CAUSAL_LM",    # Kausales Sprachmodell
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# LoRA-Adapter an das Modell heften
model = get_peft_model(model, lora_config)
print(f"Trainierbare Parameter: "
      f"{model.num_parameters(only_trainable=True):,} "
      f"von {model.num_parameters():,} "
      f"({model.num_parameters(only_trainable=True) / model.num_parameters():.2%})")

