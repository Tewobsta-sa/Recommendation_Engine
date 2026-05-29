from app import features  
from app.features import build_feature_vector  
import joblib  
import os  
from app.config import MODEL_PATH, MIN_TRAINING_SAMPLES  
import pandas as pd  
  
WEIGHTS = [  
    0.09,  # curriculum  
    0.15,  # budget  
    0.11,  # distance  
    0.10,  # rating  
    0.05,  # facilities  
    0.04,  # verification  
    0.05,  # school type  
    0.07,  # school level  
    0.05,  # passing rate  
    0.05,  # national exam  
    # New features  
    0.01,  # total students  
    0.01,  # gender balance  
    0.05,  # achievement score  
    0.03,  # achievement count  
    0.05,  # staff quality  
    0.04,  # follower count  
    0.02,  # review count  
    0.03,  # total achievement score  
]  
  
def calculate_score(features):  
    return (  
        sum(  
            feature * weight  
            for feature, weight  
            in zip(features, WEIGHTS)  
        )  
        * 100  
    )  
  
def load_ml_model():  
    """Load ML model if it exists and has sufficient training data"""  
    if not os.path.exists(MODEL_PATH):  
        return None, "Model file not found"  
      
    try:  
        model = joblib.load(MODEL_PATH)  
        # Check if model has training data info  
        if hasattr(model, 'n_samples_'):  
            if model.n_samples_ < MIN_TRAINING_SAMPLES:  
                return None, f"Insufficient training samples: {model.n_samples_} < {MIN_TRAINING_SAMPLES}"  
        return model, "Model loaded successfully"  
    except Exception as e:  
        return None, f"Error loading model: {str(e)}"  
  
def calculate_ml_score(features, model):  
    """Calculate score using ML model"""  
    import numpy as np  
    feature_array = np.array(features).reshape(1, -1)  
    probability = model.predict_proba(feature_array)[0][1]  # Probability of positive class  
    return probability * 100  
  
def rank_schools(payload):  
    schools = payload["schools"]  
    prefs = payload["preferences"]  
      
    # Try to load ML model  
    ml_model, model_status = load_ml_model()  
    use_ml = ml_model is not None  
      
    ranked = []  
      
    for school in schools:  
        school_data = dict(school)  
          
        features = build_feature_vector(  
            school_data,  
            prefs  
        )  
          
        if use_ml:  
            score = calculate_ml_score(features, ml_model)  
            scoring_method = "ml"  
        else:  
            score = calculate_score(features)  
            scoring_method = "weighted"  
          
        print(f"School: {school_data['name']}, Score: {score}, Method: {scoring_method}")    
        print(f"Features: {features}")  
        ranked.append({  
            "school_id": school_data["id"],  
            "score": round(score, 2),  
            "scoring_method": scoring_method,  
            "features": {  
                "scores": {  
                    "curriculum": features[0],  
                    "budget": features[1],  
                    "distance": features[2],  
                    "rating": features[3],  
                    "facilities": features[4],  
                    "verification": features[5],  
                    "school_type": features[6],  
                    "school_level": features[7],  
                    "passing_rate": features[8],  
                    "national_exam": features[9],  
                    # New features  
                    "total_students": features[10],  
                    "gender_balance": features[11],  
                    "achievement_score": features[12],  
                    "achievement_count": features[13],  
                    "staff_quality": features[14],  
                    "follower_count": features[15],  
                    "review_count": features[16],  
                    "total_achievement_score": features[17],  
                },  
                "final_score": round(score, 2),  
                "raw_data": {  
                    "tuition_fee": school_data["tuition_fee"],  
                    "rating": school_data["rating"],  
                    "curriculum": school_data["curriculum"],  
                    "school_type": school_data.get("school_type"),  
                    "school_level": school_data.get("school_level"),  
                    "passing_rate": school_data.get("passing_rate"),  
                    "national_exam_score": school_data.get("national_exam_score"),  
                    # New raw data  
                    "total_students": school_data.get("total_students"),  
                    "gender_balance_index": school_data.get("gender_balance_index"),  
                    "achievement_score": school_data.get("achievement_score"),  
                    "achievement_count": school_data.get("achievement_count"),  
                    "staff_quality_score": school_data.get("staff_quality_score"),  
                    "follower_count": school_data.get("follower_count"),  
                    "review_count": school_data.get("review_count"),  
                    "total_achievement_score": school_data.get("total_achievement_score"),  
                }  
            }  
        })  
      
    ranked.sort(  
        key=lambda x: x["score"],  
        reverse=True  
    )  
      
    return ranked  
  
def get_model_status():  
    """Get current model status for monitoring"""  
    ml_model, model_status = load_ml_model()  
      
    # Check training data size  
    training_data_path = "data/training_dataset.csv"  
    training_samples = 0  
    if os.path.exists(training_data_path):  
        try:  
            df = pd.read_csv(training_data_path)  
            training_samples = len(df)  
        except:  
            pass  
      
    return {  
        "ml_model_available": ml_model is not None,  
        "model_status": model_status,  
        "training_samples": training_samples,  
        "min_required_samples": MIN_TRAINING_SAMPLES,  
        "using_ml": ml_model is not None and training_samples >= MIN_TRAINING_SAMPLES  
    }