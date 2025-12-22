"""Password scoring heuristics."""

def score_password(password, company, city, current_year):
    """Score a password by likelihood of being used (higher = more likely)."""
    if not password:
        return 0

    score = 0
    pw_lower = password.lower()
    company_lower = company.lower() if company else ""
    city_lower = city.lower() if city else ""
    recent_years = {str(current_year - 1), str(current_year), str(current_year + 1)}
    recent_year_suffixes = {str(current_year - 1)[2:], str(current_year)[2:], str(current_year + 1)[2:]}

    # High-value base words
    if pw_lower.startswith("password"):
        score += 100
    if company_lower and pw_lower.startswith(company_lower):
        score += 80
    if company_lower and company_lower in pw_lower:
        score += 25

    # Season words are very common
    seasons = ["spring", "summer", "winter", "fall", "autumn"]
    for season in seasons:
        if pw_lower.startswith(season):
            score += 70
            break

    # City is moderately common
    if city_lower and pw_lower.startswith(city_lower):
        score += 50
    if city_lower and city_lower in pw_lower:
        score += 15

    # @ symbol is a common substitution
    if "@" in password:
        score += 25

    # Recent years are more likely
    for year in range(current_year - 1, current_year + 2):
        if str(year) in password:
            score += 30
            break
        if str(year)[2:] in password:  # Short year like "24"
            score += 20
            break

    # Simple suffixes are most common
    common_suffixes = [
        ("1", 40),
        ("!", 35),
        ("123", 30),
        ("123!", 28),
        ("2024", 22),
        ("2023", 18),
        ("2025", 18),
    ]
    for suffix, weight in common_suffixes:
        if password.endswith(suffix):
            score += weight
            break

    # Penalize longer/complex suffixes
    if password.endswith("1234567"):
        score -= 10

    # Common one-offs get a boost
    common_oneoffs = ["Password1", "P@ssw0rd"]
    if password == "Password1":
        score += 1000
    elif password in common_oneoffs:
        score += 50

    # Proper capitalization is more common
    if len(password) > 1 and password[0].isupper() and password[1:].islower():
        score += 12
    elif password[0].isupper():
        score += 6

    # Prefer common separator patterns (company or season + year + suffix)
    if any(token in pw_lower for token in [company_lower, city_lower, "spring", "summer", "fall", "autumn", "winter"]):
        if any(ch.isdigit() for ch in password):
            score += 10
        if any(ch in "!@#$" for ch in password):
            score += 6

    # Hard-boost seasonal patterns: <season>@<year> and <season><year>!
    for season in seasons:
        for year in recent_years:
            if pw_lower == f"{season}@{year}":
                score += 500
            if pw_lower == f"{season}{year}!":
                score += 500
        for yr in recent_year_suffixes:
            if pw_lower == f"{season}@{yr}":
                score += 480
            if pw_lower == f"{season}{yr}!":
                score += 480

    # Boost common company/year patterns near the end of the string
    if company_lower and company_lower in pw_lower:
        for year in recent_years:
            if pw_lower.endswith(year):
                score += 16
                break
            if any(pw_lower.endswith(f"{year}{suffix}") for suffix in ("!", "1", "@", "#", "$")):
                score += 20
                break
        for yr in recent_year_suffixes:
            if pw_lower.endswith(yr):
                score += 10
                break
            if any(pw_lower.endswith(f"{yr}{suffix}") for suffix in ("!", "1", "@", "#", "$")):
                score += 14
                break

    # De-prioritize weak patterns: <company>@<year>@/#/$
    if company_lower:
        for year in recent_years | recent_year_suffixes:
            if pw_lower == f"{company_lower}@{year}@" or pw_lower == f"{company_lower}@{year}#" or pw_lower == f"{company_lower}@{year}$":
                score -= 80

    # Shorter passwords slightly more common
    if len(password) <= 10:
        score += 5
    elif len(password) >= 20:
        score -= 5

    return score
