import requests  
import pandas as pd  
import os  
from app.trainer import train_model  
from app.config import BACKEND_API_URL, TRAINING_DATA_PATH, FEEDBACK_PATH  
from app.feedback_store import save_feedback  
  
def fetch_training_data():  
    """Fetch training data from backend API"""  
    try:  
        response = requests.get(f"{BACKEND_API_URL}/api/training-data", timeout=30)  
        response.raise_for_status()  
        payload = response.json()  
        training_rows = payload["data"]  
          
        # Convert to DataFrame  
        df = pd.DataFrame(training_rows)  
          
        # Save to training data file  
        os.makedirs(os.path.dirname(TRAINING_DATA_PATH), exist_ok=True)  
        df.to_csv(TRAINING_DATA_PATH, index=False)  
          
        return {  
            "success": True,  
            "samples": len(df),  
            "message": f"Fetched {len(df)} training samples"  
        }  
    except Exception as e:  
        return {  
            "success": False,  
            "error": str(e),  
            "samples": 0  
        }  
  
def merge_feedback_data():  
    """Merge feedback data with training data"""  
    if not os.path.exists(FEEDBACK_PATH):  
        return {"success": True, "message": "No feedback data to merge"}  
      
    try:  
        # Read feedback data  
        feedback_df = pd.read_csv(FEEDBACK_PATH)  
          
        if len(feedback_df) == 0:  
            return {"success": True, "message": "Feedback file is empty"}  
          
        # Transform feedback to training format  
        training_rows = []  
        for _, row in feedback_df.iterrows():  
            # Extract features from feedback if available  
            # This depends on your feedback schema  
            # For now, we'll skip if features aren't in feedback  
            if 'features' in row and row['features']:  
                features = row['features']  
                outcome = 1 if row.get('result') == 'OPENED' else 0  
                training_rows.append({  
                    **features,  
                    'outcome': outcome  
                })  
          
        if not training_rows:  
            return {"success": True, "message": "No valid feedback rows to merge"}  
          
        # Read existing training data  
        if os.path.exists(TRAINING_DATA_PATH):  
            existing_df = pd.read_csv(TRAINING_DATA_PATH)  
            merged_df = pd.concat([existing_df, pd.DataFrame(training_rows)], ignore_index=True)  
        else:  
            merged_df = pd.DataFrame(training_rows)  
          
        # Save merged data  
        os.makedirs(os.path.dirname(TRAINING_DATA_PATH), exist_ok=True)  
        merged_df.to_csv(TRAINING_DATA_PATH, index=False)  
          
        # Clear feedback file after successful merge  
        os.remove(FEEDBACK_PATH)  
          
        return {  
            "success": True,  
            "message": f"Merged {len(training_rows)} feedback samples",  
            "total_samples": len(merged_df)  
        }  
          
    except Exception as e:  
        return {  
            "success": False,  
            "error": str(e)  
        }  
  
def run_auto_training():  
    """Run complete automated training pipeline"""  
    print("Starting automated training pipeline...")  
      
    # Step 1: Fetch training data from backend  
    print("Step 1: Fetching training data from backend...")  
    fetch_result = fetch_training_data()  
    print(f"Fetch result: {fetch_result}")  
      
    # Step 2: Merge feedback data  
    print("Step 2: Merging feedback data...")  
    merge_result = merge_feedback_data()  
    print(f"Merge result: {merge_result}")  
      
    # Step 3: Train model  
    print("Step 3: Training model...")  
    train_result = train_model()  
    print(f"Training result: {train_result}")  
      
    return {  
        "fetch_result": fetch_result,  
        "merge_result": merge_result,  
        "train_result": train_result  
    }  
  
if __name__ == "__main__":  
    run_auto_training()