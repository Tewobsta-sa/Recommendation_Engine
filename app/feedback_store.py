import pandas as pd
import os

from app.config import FEEDBACK_PATH


def save_feedback(data):
    df = pd.DataFrame([data])

    file_exists = os.path.exists(FEEDBACK_PATH)

    df.to_csv(
        FEEDBACK_PATH,
        mode="a",
        header=not file_exists,
        index=False
    )