"""Password scoring heuristics."""

def score_password(password, company, city, current_year):
    """Score a password by likelihood of being used (higher = more likely)."""
    score = 0
    pw_lower = password.lower()

    # High-value base words
    if pw_lower.startswith("password"):
        score += 100
    if company and pw_lower.startswith(company.lower()):
        score += 80

    # Season words are very common
    seasons = ["spring", "summer", "winter", "fall", "autumn"]
    for season in seasons:
        if pw_lower.startswith(season):
            score += 70
            break

    # City is moderately common
    if city and pw_lower.startswith(city.lower()):
        score += 50

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
    if password.endswith("1"):
        score += 40
    elif password.endswith("!"):
        score += 35
    elif password.endswith("123"):
        score += 30
    elif password.endswith("123!"):
        score += 28

    # Penalize longer/complex suffixes
    if password.endswith("1234567"):
        score -= 10

    # Common one-offs get a boost
    common_oneoffs = ["Password1", "P@ssw0rd"]
    if password in common_oneoffs:
        score += 50

    # Proper capitalization is more common
    if password[0].isupper() and password[1:].islower() == False:
        score += 5
    if password[0].isupper():
        score += 10

    # Shorter passwords slightly more common
    if len(password) <= 10:
        score += 5

    return score
