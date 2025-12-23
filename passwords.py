import sys
import argparse
from datetime import datetime
"""Program to generate custom password lists"""

from scoring import score_password

# Suffix configuration
BASE_SPECIALS = ["!", "@", "#", "$"]
TRAILING_1 = ["1"]  # Only added to bare words, not after years/sequences

def add_variants(results, base, suffixes):
    """Add base word with all suffix combinations"""
    results.add(base)
    for suffix in suffixes:
        results.add(f"{base}{suffix}")


def create_password_list(company, include_seasons=True, base_year=None, year_range=2, city=None):
    if not company or not str(company).strip():
        raise ValueError("company must be a non-empty string")

    company = str(company).strip()
    city = str(city).strip() if city and str(city).strip() else None

    if base_year is None:
        base_year = datetime.now().year - 1
    
    current_year = datetime.now().year
    
    one_offs = ["welcome", "letmein", "Password", "P@ssw0rd"]
    season_words = ["spring", "summer", "winter", "fall", "autumn"]
    results = set()
    
    words = ["password", company.lower(), company.capitalize()]
    
    if include_seasons:
        words += season_words
    
    if city:
        words += [city, city.lower(), city.capitalize()]
    
    results.update(one_offs)
    
    for word in words:
        variants = [word, word.lower(), word.capitalize()]
        
        for variant in variants:
            # Bare word + specials (including "1" here)
            add_variants(results, variant, BASE_SPECIALS + TRAILING_1)
            
            # Year-based combinations (no trailing "1")
            for year in range(base_year, base_year + year_range + 1):
                yr = str(year)
                add_variants(results, f"{variant}{yr}", BASE_SPECIALS)
                add_variants(results, f"{variant}@{yr}", BASE_SPECIALS)
            
            # Number sequences (no trailing "1")
            numbers = ""
            for k in range(1, 8):
                numbers += str(k)
                if len(numbers) == 3:
                    add_variants(results, f"{variant}{numbers}", BASE_SPECIALS)
                    add_variants(results, f"{variant}@{numbers}", BASE_SPECIALS)
                elif len(numbers) > 3:
                    results.add(f"{variant}{numbers}")
                    results.add(f"{variant}@{numbers}")
    
    sorted_results = sorted(
        results,
        key=lambda p: (-score_password(p, company, city, current_year), p)
    )
    
    return sorted_results


def main():
    parser = argparse.ArgumentParser(description="Generate custom password lists")
    parser.add_argument("company", help="Company name to include in passwords")
    parser.add_argument("-c", "--city", help="City name to include")
    parser.add_argument("-y", "--year", type=int, default=None, 
                        help=f"Base year (default: {datetime.now().year - 1})")
    parser.add_argument("-r", "--range", type=int, default=2, dest="year_range",
                        help="Year range to generate (default: 2)")
    parser.add_argument("--no-seasons", action="store_true", 
                        help="Exclude season words")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()

    if not args.company.strip():
        print("Company name must be non-empty.", file=sys.stderr)
        return 1
    
    passwords = create_password_list(
        company=args.company,
        include_seasons=not args.no_seasons,
        base_year=args.year,
        year_range=args.year_range,
        city=args.city
    )
    
    if args.output:
        with open(args.output, "w") as f:
            f.write("\n".join(passwords))
        print(f"Generated {len(passwords)} passwords to {args.output}")
    else:
        for password in passwords:
            print(password)
    return 0


if __name__ == "__main__":
    sys.exit(main())
