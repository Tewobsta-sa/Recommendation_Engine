from math import radians, cos, sin, asin, sqrt


def curriculum_score(school, prefs):
    pref_curriculum = prefs.get("curriculum")
    if not pref_curriculum:
        return 0.5
    return (
        1.0
        if school["curriculum"].upper() == pref_curriculum.upper()
        else 0.0
    )


def budget_score(tuition, prefs):
    min_budget = prefs.get("min_budget")
    max_budget = prefs.get("max_budget")

    if min_budget is None or max_budget is None:
        return 0.5

    if max_budget <= 0:
        return 0.5

    if min_budget <= tuition <= max_budget:
        return 1.0

    difference = min(
        abs(tuition - min_budget),
        abs(tuition - max_budget)
    )

    return max(0, 1 - (difference / max_budget))


def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(
        radians,
        [lon1, lat1, lon2, lat2]
    )

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return 6371 * c


def distance_score(school, prefs):
    lat = prefs.get("lat")
    lng = prefs.get("lng")

    if lat is None or lng is None:
        return 0.5

    distance = haversine(
        lat,
        lng,
        school["latitude"],
        school["longitude"]
    )

    max_distance = prefs.get("distance_km") or 25

    if distance <= max_distance:
        return 1.0

    return max(0, 1 - (distance / 100))


def facilities_score(school):
    facilities = school.get("facilities") or ""
    if not facilities.strip():
        return 0.0

    items = facilities.split(",")

    return min(len(items), 5) / 5.0


def verification_score(school):
    return (
        1.0
        if school.get("verification_status") == "verified"
        else 0.4
    )


def school_type_score(school, prefs):  
    pref_type = prefs.get("school_type")  
    if not pref_type:  
        return 0.5  # Neutral if no preference  
    return 1.0 if school.get("school_type") == pref_type else 0.0  


def passing_rate_score(school):  
    # Normalize 0-100 to 0.0-1.0  
    return school.get("passing_rate", 0) / 100.0  


def national_exam_score(school):  
    # Normalize 0-100 to 0.0-1.0  
    return school.get("national_exam_score", 0) / 100.0


# New scoring functions for additional metrics
def total_students_score(school):
    # Normalize student count: assume reasonable range 100-5000
    total = school.get("total_students", 0)
    if total == 0:
        return 0.5
    # Logarithmic scaling to handle wide range
    import math
    normalized = math.log(max(total, 1)) / math.log(5000)
    return min(normalized, 1.0)


def gender_balance_score(school):
    # gender_balance_index is already 0-1 (1 = perfect balance)
    return school.get("gender_balance_index", 0.5)


def achievement_score(school):
    # achievement_score is already normalized 0-1
    return school.get("achievement_score", 0.0) /100.0


def achievement_count_score(school):
    # Normalize count: assume reasonable range 0-50
    count = school.get("achievement_count", 0)
    return min(count / 50.0, 1.0)


def staff_quality_score(school):
    # staff_quality_score is already normalized 0-1
    return school.get("staff_quality_score", 0.0)


def follower_count_score(school):
    # Normalize follower count: assume reasonable range 0-1000
    followers = school.get("follower_count", 0)
    return min(followers / 1000.0, 1.0)


def review_count_score(school):
    # Normalize review count: assume reasonable range 0-500
    reviews = school.get("review_count", 0)
    return min(reviews / 500.0, 1.0)


def total_achievement_score(school):
    # total_achievement_score is already normalized 0-1
    return school.get("total_achievement_score", 0.0)



def build_feature_vector(school, prefs):
    return [
        curriculum_score(school, prefs),
        budget_score(school["tuition_fee"], prefs),
        distance_score(school, prefs),
        school["rating"] / 5.0,  # This matches API's rating_score
        facilities_score(school),
        verification_score(school),
        school_type_score(school, prefs),
        # school_level_score removed - not provided by API
        passing_rate_score(school),
        national_exam_score(school),
        # New features
        total_students_score(school),
        gender_balance_score(school),
        achievement_score(school),  # Renamed from achievement_score_normalized
        achievement_count_score(school),
        staff_quality_score(school),  # Renamed from staff_quality_score_normalized
        follower_count_score(school),
        review_count_score(school),
        total_achievement_score(school),  # Renamed from total_achievement_score_normalized
    ]
