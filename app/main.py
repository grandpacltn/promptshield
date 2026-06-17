from fastapi import FastAPI
from pydantic import BaseModel
from app.detector import detect_injection

app = FastAPI(title="PromptShield API", version="0.1.0")

class PromptRequest(BaseModel):
    prompt: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    matched_pattern: str | None

@app.get("/health")
def health_check():
    return {"status": "ok", "model": "rule-based-v1"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PromptRequest):
    result = detect_injection(request.prompt)
    return result