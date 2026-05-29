from fastapi import FastAPI  
from fastapi.responses import JSONResponse  
from app.model import rank_schools, get_model_status  
from app.schemas import (  
    RecommendationRequest,  
    FeedbackRequest  
)  
from app.feedback_store import save_feedback  
from app.auto_trainer import run_auto_training  
from apscheduler.schedulers.background import BackgroundScheduler  
from app.config import RETRAIN_INTERVAL_HOURS  
import logging  
  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
  
app = FastAPI()  
  
# Initialize background scheduler  
scheduler = BackgroundScheduler()  
  
@app.on_event("startup")  
def startup_event():  
    """Initialize scheduled tasks on startup"""  
    try:  
        # Schedule automatic retraining  
        scheduler.add_job(  
            run_auto_training,  
            'interval',  
            hours=RETRAIN_INTERVAL_HOURS,  
            id='auto_training',  
            name='Automatic Model Training'  
        )  
        scheduler.start()  
        logger.info(f"Scheduler started - Auto retraining every {RETRAIN_INTERVAL_HOURS} hours")  
    except Exception as e:  
        logger.error(f"Failed to start scheduler: {e}")  
  
@app.on_event("shutdown")  
def shutdown_event():  
    """Cleanup on shutdown"""  
    scheduler.shutdown()  
  
@app.get("/health")  
def health():  
    return {"status": "ok"}  
  
@app.get("/model-status")  
def model_status():  
    """Get current ML model status"""  
    return get_model_status()  
  
@app.post("/recommend")  
def recommend(payload: RecommendationRequest):  
    raw_payload = payload.model_dump()  
      
    ranked = rank_schools(raw_payload)  
    return JSONResponse(content={"ranked": ranked})  
  
@app.post("/feedback")  
def feedback(payload: FeedbackRequest):  
    save_feedback(payload.model_dump())  
  
    return {  
        "message": "feedback stored"  
    }  
  
@app.post("/retrain")  
def retrain():  
    """Manually trigger model retraining"""  
    try:  
        result = run_auto_training()  
        return JSONResponse(content={  
            "success": True,  
            "result": result  
        })  
    except Exception as e:  
        return JSONResponse(content={  
            "success": False,  
            "error": str(e)  
        }, status_code=500)