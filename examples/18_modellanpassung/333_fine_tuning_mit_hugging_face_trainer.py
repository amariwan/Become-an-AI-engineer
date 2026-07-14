# Fine-Tuning mit Hugging Face Trainer
# Quelle: chapters/18_modellanpassung.tex (Zeile 333)
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./lora-llama-sql",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,   # Effektive Batch-Size: 32
    learning_rate=2e-4,
    warmup_steps=100,
    num_train_epochs=3,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    fp16=True,
    report_to="wandb",              # Experiment-Tracking
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset_dict["train"],
    eval_dataset=dataset_dict["test"],
    tokenizer=tokenizer,
    data_collator=lambda data: tokenizer.pad(
        [{"text": format_chat(d["messages"])} for d in data],
        return_tensors="pt",
    ),
)

trainer.train()

