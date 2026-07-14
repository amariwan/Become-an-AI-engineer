# Fine-Tuning mit OpenAI
# Quelle: chapters/05_openai_plattform.tex (Zeile 454)
import json

# Schritt 1: Trainingsdaten hochladen (JSONL)
with open("training_data.jsonl", "w") as f:
    for msg_set in [
        {"messages": [
            {"role": "user",
             "content": "Wie heisst du?"},
            {"role": "assistant",
             "content": "Ich bin FinanzBot."}]},
        {"messages": [
            {"role": "user",
             "content": "Was kostet der Tarif?"},
            {"role": "assistant",
             "content": "Der Preis ist 29 EUR/Monat."}]},
    ]:
        f.write(json.dumps(msg_set) + "\n")

upload = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Schritt 2: Fine-Tuning Job starten
ft_job = client.fine_tuning.jobs.create(
    training_file=upload.id,
    model="gpt-4o-mini",
    hyperparameters={
        "n_epochs": 3,
        "learning_rate_multiplier": 0.1,
    },
)

# Schritt 3: Fertiges Modell nutzen
fine_tuned_model = ft_job.fine_tuned_model
response = client.chat.completions.create(
    model=fine_tuned_model,
    messages=[{"role": "user", "content": "Wie heisst du?"}],
)

