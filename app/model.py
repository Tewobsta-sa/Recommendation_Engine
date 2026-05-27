from app import features
from app.features import build_feature_vector

WEIGHTS = [
    0.15,  # curriculum
    0.15,  # budget
    0.12,  # distance
    0.10,  # rating
    0.06,  # facilities
    0.04,  # verification
    0.03,  # school type
    0.03,  # school level
    0.03,  # passing rate
    0.02,  # national exam
    # New features
    0.08,  # total students
    0.06,  # gender balance
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


def rank_schools(payload):
    schools = payload["schools"]
    prefs = payload["preferences"]

    ranked = []

    for school in schools:
        school_data = dict(school)

        features = build_feature_vector(
            school_data,
            prefs
        )

        score = calculate_score(features)

        print(f"School: {school_data['name']}, Score: {score}")  
        print(f"Features: {features}")
        ranked.append({
            "school_id": school_data["id"],
            "score": round(score, 2),
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
