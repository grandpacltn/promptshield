FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY models/ ./models/
COPY dataset.csv .
COPY app/train_models.py .

RUN python train_models.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]