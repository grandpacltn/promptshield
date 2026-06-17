import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, matthews_corrcoef, classification_report
)
import pickle

# ── 1. Load dataset ──
print("Loading dataset...")
df = pd.read_csv("dataset.csv")
X = df["prompt"]
y = df["label"]

# ── 2. Split ──
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# ── 3. Evaluation function ──
def evaluate(name, y_true, y_pred):
    print(f"\n{'='*40}")
    print(f"Model: {name}")
    print(f"{'='*40}")
    print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")
    print(f"MCC:       {matthews_corrcoef(y_true, y_pred):.4f}")
    print(f"\n{classification_report(y_true, y_pred)}")

# ── 4. Random Forest ──
print("\nTraining Random Forest...")
rf_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000)),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])
rf_pipeline.fit(X_train, y_train)
rf_pred = rf_pipeline.predict(X_test)
evaluate("Random Forest", y_test, rf_pred)

# ── 5. XGBoost ──
print("\nTraining XGBoost...")
xgb_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000)),
    ("clf", XGBClassifier(n_estimators=100, random_state=42,
                          eval_metric="logloss", verbosity=0))
])
xgb_pipeline.fit(X_train, y_train)
xgb_pred = xgb_pipeline.predict(X_test)
evaluate("XGBoost", y_test, xgb_pred)

# ── 6. Save models ──
print("\nSaving models...")
with open("models/random_forest.pkl", "wb") as f:
    pickle.dump(rf_pipeline, f)
with open("models/xgboost.pkl", "wb") as f:
    pickle.dump(xgb_pipeline, f)