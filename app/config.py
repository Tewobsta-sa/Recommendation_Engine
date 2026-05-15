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