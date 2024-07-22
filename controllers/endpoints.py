from fastapi import APIRouter, HTTPException, Form, Request
from pydantic import BaseModel
from typing import Dict

from solutions.question_one import analyze_sentiment
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze_sentiment", response_model=SentimentResponse)
@limiter.limit("5/minute")
async def sentiment_analysis_endpoint(request: Request, text: str = Form(...)):
    try:
        input_data = SentimentRequest(text=text)
        result = analyze_sentiment(input_data.text)
        return SentimentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during sentiment analysis: {str(e)}")
