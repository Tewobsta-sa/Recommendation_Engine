import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import accuracy_score


DATASET_PATH = (
    "data/training_dataset.csv"
)

MODEL_PATH = (
    "models/recommender.pkl"
)

# STEP 1
# Load dataset
df = pd.read_csv(DATASET_PATH)

# STEP 2
# Features
X = df.drop(columns=["outcome"])

# STEP 3
# Labels
y = df["outcome"]

# STEP 4
# Split dataset
X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )
)

# STEP 5
# Train model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# STEP 6
# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Accuracy: {accuracy}")

# STEP 7
# Save model
joblib.dump(
    model,
    MODEL_PATH
)

print("Model saved")