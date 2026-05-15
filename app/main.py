from fastapi import FastAPI
from app.model import rank_schools
from app.schemas import (
    RecommendationRequest,
    FeedbackRequest
)
from app.feedback_store import save_feedback

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend(payload: RecommendationRequest):
    ranked = rank_schools(payload.dict())

    return {
        "ranked": ranked
    }


@app.post("/feedback")
def feedback(payload: FeedbackRequest):
    save_feedback(payload.dict())

    return {
        "message": "feedback stored"
    }