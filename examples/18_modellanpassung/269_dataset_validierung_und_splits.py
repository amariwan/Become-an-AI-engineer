# Dataset-Validierung und Splits
# Quelle: chapters/18_modellanpassung.tex (Zeile 269)
from datasets import Dataset, DatasetDict

# Dataset splitten
dataset = Dataset.from_list(DATASET)
splits = dataset.train_test_split(test_size=0.1, seed=42)

dataset_dict = DatasetDict({
    "train": splits["train"],
    "test": splits["test"],
})

# Qualitaetscheck: Token-Laenge pro Beispiel
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-3.2-8B-Instruct"
)

def token_length(example):
    # Nur Assistant-Tokens zaehlen (Output-Learning)
    assistant_text = [
        msg["content"] for msg in example["messages"]
        if msg["role"] == "assistant"
    ][0]
    tokens = tokenizer(assistant_text, truncation=True)
    example["assistant_tokens"] = len(tokens["input_ids"])
    return example

dataset = dataset.map(token_length)

# Verteilung der Output-Laengen prüfen
lengths = dataset["assistant_tokens"]
print(f"Min: {min(lengths)}, Max: {max(lengths)}, "
      f"Avg: {sum(lengths)/len(lengths):.0f}")

# Warnung bei zu kurzen Outputs
if sum(1 for l in lengths if l < 10) > len(lengths) * 0.1:
    print("WARN: Ueber 10% der Outputs haben <10 Tokens")

