from app.features import build_feature_vector

WEIGHTS = [
    0.25,
    0.25,
    0.20,
    0.15,
    0.10,
    0.05,
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
            "breakdown": {
                "curriculum": features[0],
                "budget": features[1],
                "distance": features[2],
                "rating": features[3],
                "facilities": features[4],
                "verification": features[5],
            }
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked