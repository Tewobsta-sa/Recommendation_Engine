from math import radians, cos, sin, asin, sqrt


def curriculum_score(school, prefs):
    pref_cur = prefs.get("curriculum")
    if not pref_cur:
        return 0.5
    return (
        1.0
        if school["curriculum"] == pref_cur
        else 0.0
    )


def budget_score(tuition, prefs):
    min_budget = prefs.get("min_budget") or 0
    max_budget = prefs.get("max_budget") or 100000

    if max_budget <= 0:
        max_budget = 100000

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
    if lat is None or lng is None or (lat == 0 and lng == 0):
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
    facilities = school["facilities"].split(",")

    return min(len(facilities), 5) / 5.0


def verification_score(school):
    return (
        1.0
        if school["verification_status"] == "verified"
        else 0.4
    )


def build_feature_vector(school, prefs):
    return [
        curriculum_score(school, prefs),
        budget_score(school["tuition_fee"], prefs),
        distance_score(school, prefs),
        school["rating"] / 5.0,
        facilities_score(school),
        verification_score(school),
    ]