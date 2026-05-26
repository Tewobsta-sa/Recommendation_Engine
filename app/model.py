from app.features import build_feature_vector

WEIGHTS = [
    0.22,  # curriculum
    0.22,  # budget
    0.18,  # distance
    0.14,  # rating
    0.08,  # facilities
    0.05,  # verification
    0.04,  # school type
    0.04,  # passing rate
    0.03,  # national exam
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
        "passing_rate": features[7],
        "national_exam": features[8],
    },

    "final_score": round(score, 2),

    "raw_data": {
        "tuition_fee": school_data["tuition_fee"],
        "rating": school_data["rating"],
        "curriculum": school_data["curriculum"],
        "school_type": school_data.get("school_type"),
        "passing_rate": school_data.get("passing_rate"),
    }
}
})

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked