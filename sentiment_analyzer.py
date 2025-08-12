# sentiment_analyzer.py
from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text):
    if not text or not isinstance(text, str):
        return {'label': 'NEUTRAL', 'score': 0.5}
    try:
        return sentiment_pipeline(text)[0]
    except Exception:
        return {'label': 'NEUTRAL', 'score': 0.5}