"""
Country/Region-based language and region style mapping.
Maps user's region to their preferred language and regional roasting style.
Supports both countries and specific regions/cities.
"""

# Mapping of region/country to (primary_language, region_style)
REGION_LANGUAGE_MAP = {
    # Default
    "Delhi": ("Hindi + English (Hinglish)", "Delhi/North Indian street roast"),
    
    # India - Cities/Regions
    "Mumbai": ("Hindi + Marathi + English (Hinglish)", "Mumbai tapori"),
    "Bombay": ("Hindi + English (Hinglish)", "Mumbai tapori"),
    "Bangalore": ("Kannada + English", "Bangalore tech humor"),
    "Bengaluru": ("Kannada + English", "Bangalore tech humor"),
    "Chennai": ("Tamil + English", "Chennai South Indian style"),
    "Madras": ("Tamil + English", "Chennai South Indian style"),
    "Kolkata": ("Bengali + English", "Kolkata intellectual roast"),
    "Calcutta": ("Bengali + English", "Kolkata intellectual roast"),
    "Hyderabad": ("Telugu + English", "Hyderabad tech swagger"),
    "Pune": ("Marathi + English", "Pune attitude"),
    "Hyderabad": ("Telugu + English", "Hyderabad tech swagger"),
    "Gurgaon": ("Hindi + English (Hinglish)", "Gurgaon corporate roast"),
    "Noida": ("Hindi + English (Hinglish)", "Delhi/North Indian street roast"),
    "Indore": ("Hindi", "Indore street style"),
    "Jaipur": ("Hindi", "Jaipur royal roast"),
    "Lucknow": ("Urdu + Hindi", "Lucknow Awadhi style"),
    "Ahmedabad": ("Gujarati + English", "Ahmedabad Gujarati humor"),
    "Surat": ("Gujarati + English", "Surat diamond city swagger"),
    "Chandigarh": ("Punjabi + English", "Chandigarh Punjabi swagger"),
    "Mohali": ("Punjabi + English", "Chandigarh Punjabi swagger"),
    "Amritsar": ("Punjabi", "Punjab Punjabi roast"),
    "Ludhiana": ("Punjabi", "Punjab Punjabi roast"),
    "Goa": ("Konkani + English", "Goa beach vibes"),
    "Panaji": ("Konkani + English", "Goa beach vibes"),
    "Kochi": ("Malayalam + English", "Kochi Kerala style"),
    "Cochin": ("Malayalam + English", "Kochi Kerala style"),
    "Thiruvananthapuram": ("Malayalam + English", "Thiruvananthapuram Kerala style"),
    
    # Countries
    "India": ("Hindi + English (Hinglish)", "Delhi/North Indian street roast"),
    "IN": ("Hindi + English (Hinglish)", "Delhi/North Indian street roast"),
    
    # USA
    "USA": ("English", "Gen-Z internet"),
    "United States": ("English", "Gen-Z internet"),
    "US": ("English", "Gen-Z internet"),
    "New York": ("English", "New York sass"),
    "California": ("English", "California laid-back"),
    "Texas": ("English", "Texas swagger"),
    "Florida": ("English", "Florida chaos"),
    
    # UK
    "UK": ("English", "British sarcasm"),
    "United Kingdom": ("English", "British sarcasm"),
    "GB": ("English", "British sarcasm"),
    "London": ("English", "London cockney"),
    
    # Australia
    "Australia": ("English", "Australian slang"),
    "AU": ("English", "Australian slang"),
    "Sydney": ("English", "Sydney beach culture"),
    "Melbourne": ("English", "Melbourne hipster humor"),
    
    # Canada
    "Canada": ("English", "Canadian humor"),
    "CA": ("English", "Canadian humor"),
    
    # Germany
    "Germany": ("German", "German directness"),
    "DE": ("German", "German directness"),
    
    # France
    "France": ("French", "French wit"),
    "FR": ("French", "French wit"),
    
    # Spain
    "Spain": ("Spanish", "Spanish passion"),
    "ES": ("Spanish", "Spanish passion"),
    
    # Mexico
    "Mexico": ("Spanish", "Mexican street style"),
    "MX": ("Spanish", "Mexican street style"),
    
    # Brazil
    "Brazil": ("Portuguese", "Brazilian swagger"),
    "BR": ("Portuguese", "Brazilian swagger"),
    
    # Japan
    "Japan": ("Japanese", "Japanese politeness"),
    "JP": ("Japanese", "Japanese politeness"),
    
    # China
    "China": ("Mandarin", "Chinese humor"),
    "CN": ("Mandarin", "Chinese humor"),
    
    # South Korea
    "South Korea": ("Korean", "K-pop sass"),
    "Korea": ("Korean", "K-pop sass"),
    "KR": ("Korean", "K-pop sass"),
    
    # Middle East
    "Saudi Arabia": ("Arabic", "Middle Eastern style"),
    "SA": ("Arabic", "Middle Eastern style"),
    "UAE": ("Arabic", "Dubai swagger"),
    "United Arab Emirates": ("Arabic", "Dubai swagger"),
    "Dubai": ("Arabic", "Dubai swagger"),
    
    # Pakistan
    "Pakistan": ("Urdu + English", "Pakistan street style"),
    "PK": ("Urdu + English", "Pakistan street style"),
    "Karachi": ("Urdu + English", "Karachi street style"),
    "Lahore": ("Urdu + English", "Lahore Punjab style"),
    "Islamabad": ("Urdu + English", "Islamabad sophisticated"),
    
    # Bangladesh
    "Bangladesh": ("Bengali + English", "Dhaka banter"),
    "BD": ("Bengali + English", "Dhaka banter"),
    "Dhaka": ("Bengali + English", "Dhaka banter"),
    
    # Sri Lanka
    "Sri Lanka": ("Tamil + English", "Colombo style"),
    "LK": ("Tamil + English", "Colombo style"),
    "Colombo": ("Tamil + English", "Colombo style"),
    
    # Thailand
    "Thailand": ("Thai", "Thai humor"),
    "TH": ("Thai", "Thai humor"),
    "Bangkok": ("Thai", "Bangkok swagger"),
    
    # Vietnam
    "Vietnam": ("Vietnamese", "Vietnamese wit"),
    "VN": ("Vietnamese", "Vietnamese wit"),
    
    # Indonesia
    "Indonesia": ("Indonesian", "Jakarta street style"),
    "ID": ("Indonesian", "Jakarta street style"),
    "Jakarta": ("Indonesian", "Jakarta street style"),
    
    # Philippines
    "Philippines": ("English + Filipino", "Filipino banter"),
    "PH": ("English + Filipino", "Filipino banter"),
    "Manila": ("English + Filipino", "Manila street style"),
    
    # Nigeria
    "Nigeria": ("English + Pidgin", "Nigerian swagger"),
    "NG": ("English + Pidgin", "Nigerian swagger"),
    "Lagos": ("English + Pidgin", "Lagos swagger"),
    
    # South Africa
    "South Africa": ("English", "South African humor"),
    "ZA": ("English", "South African humor"),
    
    # Kenya
    "Kenya": ("English + Swahili", "Nairobi style"),
    "KE": ("English + Swahili", "Nairobi style"),
    
    # Singapore
    "Singapore": ("English + Mandarin", "Singapore sass"),
    "SG": ("English + Mandarin", "Singapore sass"),
    
    # Malaysia
    "Malaysia": ("Malay + English", "Malaysian humor"),
    "MY": ("Malay + English", "Malaysian humor"),
    
    # Russia
    "Russia": ("Russian", "Russian directness"),
    "RU": ("Russian", "Russian directness"),
    "Moscow": ("Russian", "Moscow swagger"),
    
    # Ukraine
    "Ukraine": ("Ukrainian", "Eastern European sass"),
    "UA": ("Ukrainian", "Eastern European sass"),
    
    # Poland
    "Poland": ("Polish", "Polish wit"),
    "PL": ("Polish", "Polish wit"),
    
    # Italy
    "Italy": ("Italian", "Italian passion"),
    "IT": ("Italian", "Italian passion"),
    
    # Greece
    "Greece": ("Greek", "Greek philosophy roast"),
    "GR": ("Greek", "Greek philosophy roast"),
    
    # Turkey
    "Turkey": ("Turkish", "Istanbul swagger"),
    "TR": ("Turkish", "Istanbul swagger"),
    
    # Argentina
    "Argentina": ("Spanish", "Argentine sass"),
    "AR": ("Spanish", "Argentine sass"),
    
    # Chile
    "Chile": ("Spanish", "Chilean humor"),
    "CL": ("Spanish", "Chilean humor"),
    
    # Colombia
    "Colombia": ("Spanish", "Colombian street style"),
    "CO": ("Spanish", "Colombian street style"),
}


def get_language_and_style_by_region(region: str) -> tuple[str, str]:
    """
    Get language and region style based on region/country.

    Args:
        region: Region name, city name, or ISO code (e.g., "Delhi", "Mumbai", "India", "IN", "USA", "US", "London")

    Returns:
        (language, region_style) tuple
        Falls back to ("Hindi + English (Hinglish)", "Delhi/North Indian street roast") if region not found
    """
    # Try exact match (case-sensitive first for codes, then case-insensitive for names)
    if region in REGION_LANGUAGE_MAP:
        return REGION_LANGUAGE_MAP[region]

    # Try case-insensitive match
    region_lower = region.lower()
    for key, value in REGION_LANGUAGE_MAP.items():
        if key.lower() == region_lower:
            return value

    # Fallback to Delhi default
    return ("Hindi + English (Hinglish)", "Delhi/North Indian street roast")
