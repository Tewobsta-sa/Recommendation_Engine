import pandas as pd  
import joblib  
import os  
from sklearn.ensemble import RandomForestClassifier  
from sklearn.model_selection import train_test_split  
from sklearn.metrics import accuracy_score  
from app.config import MODEL_PATH, TRAINING_DATA_PATH, MIN_TRAINING_SAMPLES  
  
def train_model():  
    """Train ML model and return results"""  
      
    # Check if training data exists  
    if not os.path.exists(TRAINING_DATA_PATH):  
        return {  
            "success": False,  
            "error": "Training data file not found",  
            "samples": 0  
        }  
      
    try:  
        # STEP 1: Load dataset  
        df = pd.read_csv(TRAINING_DATA_PATH)  
          
        # Check minimum samples  
        if len(df) < MIN_TRAINING_SAMPLES:  
            return {  
                "success": False,  
                "error": f"Insufficient training data: {len(df)} < {MIN_TRAINING_SAMPLES}",  
                "samples": len(df)  
            }  
          
        # STEP 2: Features - dynamically detect all columns except 'outcome'  
        FEATURE_COLUMNS = [col for col in df.columns if col != "outcome"]  
        X = df[FEATURE_COLUMNS]  
          
        # STEP 3: Labels  
        y = df["outcome"]  
          
        # STEP 4: Split dataset  
        X_train, X_test, y_train, y_test = train_test_split(  
            X, y,  
            test_size=0.2,  
            random_state=42  
        )  
          
        # STEP 5: Train model  
        model = RandomForestClassifier(  
            n_estimators=100,  
            max_depth=10,  
            random_state=42  
        )  
          
        model.fit(X_train, y_train)  
          
        # Store training data size in model  
        model.n_samples_ = len(df)  
        model.feature_columns_ = FEATURE_COLUMNS  
          
        # STEP 6: Evaluate  
        predictions = model.predict(X_test)  
        accuracy = accuracy_score(y_test, predictions)  
          
        # STEP 7: Save model  
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)  
        joblib.dump(model, MODEL_PATH)  
          
        return {  
            "success": True,  
            "accuracy": accuracy,  
            "samples": len(df),  
            "feature_columns": FEATURE_COLUMNS,  
            "model_path": MODEL_PATH  
        }  
          
    except Exception as e:  
        return {  
            "success": False,  
            "error": str(e),  
            "samples": 0  
        }  
  
# Keep backward compatibility for manual execution  
if __name__ == "__main__":  
    result = train_model()  
    if result["success"]:  
        print(f"Training successful! Accuracy: {result['accuracy']}")  
        print(f"Samples: {result['samples']}")  
        print(f"Feature columns: {result['feature_columns']}")  
        print("Model saved")  
    else:  
        print(f"Training failed: {result['error']}")