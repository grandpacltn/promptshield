import pandas as pd
import re
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef

INJECTION_PATTERNS = [
    r"ignore (all |previous |your )?(instructions|rules|guidelines)",
    r"disregard (all |previous |your )?(instructions|rules|guidelines)",
    r"forget (all |previous |your )?(instructions|rules|guidelines)",
    r"you are now", r"act as", r"pretend (you are|to be)",
    r"roleplay", r"no restrictions", r"unrestricted",
    r"system prompt", r"override", r"jailbreak",
    r"developer mode", r"bypass", r"do anything now",
    r"output (all|the|your) (client|data|records|database)",
]

def rule_based_predict(text):
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return 1
    return 0

df = pd.read_csv("dataset.csv")
label_col = "label" if "label" in df.columns else df.columns[1]
text_col = "prompt" if "prompt" in df.columns else df.columns[0]
y_true = df[label_col].apply(lambda x: 1 if str(x).strip() in ["1","MALICIOUS","malicious","True","true"] else 0).tolist()
texts = df[text_col].tolist()
y_pred = [rule_based_predict(str(t)) for t in texts]

accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred, zero_division=0)
mcc = matthews_corrcoef(y_true, y_pred)

print("="*50)
print("RULE-BASED CLASSIFIER RESULTS")
print("="*50)
print(f"Accuracy : {accuracy*100:.2f}%")
print(f"F1 Score : {f1:.4f}")
print(f"MCC      : {mcc:.4f}")
print("="*50)
