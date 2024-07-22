from fastapi import APIRouter, HTTPException, Form, Request
from pydantic import BaseModel
from typing import Dict

from solutions.question_one import analyze_sentiment
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from typing import Optional
from solutions.question_three.summarizer import summarize_text
from solutions.question_three.prompt_engg import enhance_prompt
from solutions.question_three.feedback_sys import collect_feedback, adjust_prompt_based_on_feedback
from solutions.question_three.evaluation import evaluate_summary

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

class SummarizationRequest(BaseModel):
    text: str
    style: Optional[str] = "paragraph"

class FeedbackRequest(BaseModel):
    feedback: str

limiter = Limiter(key_func=get_remote_address)

### Qeustion 1 endpoint

@router.post("/analyze_sentiment", response_model=SentimentResponse)
@limiter.limit("5/minute")
async def sentiment_analysis_endpoint(request: Request, text: str = Form(...)):
    try:
        input_data = SentimentRequest(text=text)
        result = analyze_sentiment(input_data.text)
        return SentimentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during sentiment analysis: {str(e)}")\
        
### Question 2 endpoint
    
@router.post("/summarize/", tags=["Summariser"])
async def summarize(request: SummarizationRequest):
    enhanced_prompt = enhance_prompt(request.text)
    summary = summarize_text(enhanced_prompt, request.style)
    return {"summary": summary}

@router.post("/feedback/", tags=["Summariser"])
async def feedback(request: FeedbackRequest):
    collect_feedback(request.feedback)
    return {"message": "Feedback received"}

@router.post("/evaluate/", tags=["Summariser"])
async def evaluate(request: SummarizationRequest):
    summary = summarize_text(request.text, request.style)
    score = evaluate_summary(request.text, summary)
    return {"score": score}
