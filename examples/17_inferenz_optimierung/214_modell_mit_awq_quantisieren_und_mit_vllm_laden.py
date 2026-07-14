# Modell mit AWQ quantisieren und mit vLLM laden
# Quelle: chapters/17_inferenz_optimierung.tex (Zeile 214)
# Quantisierung mit AutoAWQ
from awq import AutoAWQForCausalLM

model = AutoAWQForCausalLM.from_pretrained(
    "meta-llama/Llama-3.3-70B-Instruct",
)

model.quantize(
    quant_config={"zero_point": True, "q_group_size": 128, "w_bit": 4},
    calib_data="c4",  # Kalibrierungs-Dataset
)

model.save_quantized("llama-70b-awq")

