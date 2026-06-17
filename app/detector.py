import pickle
import os

# ── Load model ──
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/random_forest.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def detect_injection(prompt: str) -> dict:
    prediction = model.predict([prompt])[0]
    probability = model.predict_proba([prompt])[0]
    confidence = round(float(probability[prediction]), 4)
    label = "BLOCKED" if prediction == 1 else "ALLOWED"
    return {
        "label": label,
        "confidence": confidence,
        "matched_pattern": None
    }