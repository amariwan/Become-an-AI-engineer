# Fine-Tuning Pipeline -- Trainingsdaten erstellen und Modell trainieren
# Quelle: chapters/14_praxisprojekte.tex (Zeile 293)
import json
import openai

# === Schritt 1: Trainingsdaten erstellen (JSONL) ===
training_data = [
    {
        "messages": [
            {"role": "user", "content": "Was kostet das Enterprise-Ticket?"},
            {"role": "assistant", "content": "Das Enterprise-Ticket kostet "
             "99 EUR/Monat exkl. MwSt."}
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Kann ich das Abo kuendigen?"},
            {"role": "assistant", "content": "Ja, Sie koennen Ihr Abo "
             "jederzeit kuendigen. Gehen Sie zu Einstellungen > Abonnement."}
        ]
    },
]

with open("fine_tuning_data.jsonl", "w") as f:
    for item in training_data:
        f.write(json.dumps(item) + "\n")

# === Schritt 2: Datei hochladen ===
client = openai.OpenAI()
file_response = client.files.create(
    file=open("fine_tuning_data.jsonl", "rb"),
    purpose="fine-tune"
)

# === Schritt 3: Fine-Tuning Job starten ===
ft_job = client.fine_tuning.jobs.create(
    training_file=file_response.id,
    model="gpt-4o-mini",
    hyperparameters={"n_epochs": 3, "learning_rate_multiplier": 0.1},
)

print(f"Fine-Tuning gestartet! Job ID: {ft_job.id}")

# === Schritt 4: Evaluieren ===
def eval_fine_tuned(model_name, test_data):
    for example in test_data[:5]:
        baseline = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user",
                       "content": example["input"]}]
        ).choices[0].message.content

        fine_tuned = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user",
                       "content": example["input"]}]
        ).choices[0].message.content

        print(f"Input: {example['input'][:40]}...")
        print(f"Baseline:   {baseline[:60]}...")
        print(f"FineTuned:  {fine_tuned[:60]}...")
        print("---")

