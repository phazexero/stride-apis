from typing import Dict
from transformers import pipeline

def analyze_sentiment(text: str) -> Dict[str, float]:
    sentiment_model = pipeline("sentiment-analysis")
    
    result = sentiment_model(text)[0]
    sentiment = "positive" if result["label"] == "POSITIVE" else "negative"
    
    return {
        "sentiment": sentiment,
        "confidence": result["score"]
    }