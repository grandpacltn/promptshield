import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, matthews_corrcoef, classification_report
)
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer
)
from torch.utils.data import Dataset

# ── Check GPU ──
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# ── 1. Load dataset ──
df = pd.read_csv("dataset.csv")
X = df["prompt"].tolist()
y = df["label"].tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# ── 2. Tokenizer ──
MODEL_NAME = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# ── 3. Dataset class ──
class PromptDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

train_dataset = PromptDataset(X_train, y_train)
test_dataset = PromptDataset(X_test, y_test)

# ── 4. Model ──
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
model.to(device)

# ── 5. Training args ──
training_args = TrainingArguments(
    output_dir="./bert_output",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_strategy="epoch",
    save_strategy="no",
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=False,
    report_to="none"
)

# ── 6. Trainer ──
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

print("\nTraining BERT...")
trainer.train()

# ── 7. Evaluate ──
print("\nEvaluating...")
preds = trainer.predict(test_dataset)
y_pred = preds.predictions.argmax(axis=1)

print(f"\n{'='*40}")
print("Model: DistilBERT")
print(f"{'='*40}")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
print(f"MCC:       {matthews_corrcoef(y_test, y_pred):.4f}")
print(f"\n{classification_report(y_test, y_pred)}")

# ── 8. Save ──
model.save_pretrained("models/bert")
tokenizer.save_pretrained("models/bert")
print("✅ BERT model saved to models/bert/")