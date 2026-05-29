from dotenv import load_dotenv  
import os  
  
load_dotenv()  
  
MODEL_PATH = os.getenv(  
    "MODEL_PATH",  
    "models/recommender.pkl"  
)  
  
FEEDBACK_PATH = os.getenv(  
    "FEEDBACK_PATH",  
    "data/feedback.csv"  
)  
  
TRAINING_DATA_PATH = os.getenv(  
    "TRAINING_DATA_PATH",  
    "data/training_dataset.csv"  
)  
  
BACKEND_API_URL = os.getenv(  
    "BACKEND_API_URL",  
    "http://localhost:5050"  
)  
  
MIN_TRAINING_SAMPLES = int(os.getenv(  
    "MIN_TRAINING_SAMPLES",  
    "100"  
))  
  
RETRAIN_INTERVAL_HOURS = int(os.getenv(  
    "RETRAIN_INTERVAL_HOURS",  
    "24"  
))