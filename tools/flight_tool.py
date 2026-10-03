# import os 
# import re 
# import certifi
# import airportsdata
# import pycountry
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# os.environ["SSL_CERT_FILE"] = certifi.where()
# os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# # Default origin when user says only destination, e.g. "Japan trip"
# # Change this if your default location is not Bangladesh/Dhaka.
# DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "DEL")


# BASE_URL = "https://api.aviationstack.com/v1/flights"


# AIRPORTS = airportsdata.load("IATA")



# COUNTRY_ALIASES = {
#     "usa": "US",
#     "u.s.a": "US",
#     "u.s.": "US",
#     "america": "US",
#     "united states": "US",
#     "uk": "GB",
#     "u.k.": "GB",
#     "britain": "GB",
#     "england": "GB",
#     "uae": "AE",
#     "dubai": "AE",
#     "south korea": "KR",
#     "korea": "KR",
#     "russia": "RU",
#     "vietnam": "VN",
#     "bangladesh": "BD",
#     "india": "IN",
#     "japan": "JP",
#     "china": "CN",
#     "singapore": "SG",
#     "malaysia": "MY",
#     "thailand": "TH",
#     "indonesia": "ID",
#     "nepal": "NP",
#     "qatar": "QA",
#     "saudi arabia": "SA",
#     "turkey": "TR",
#     "canada": "CA",
#     "australia": "AU",
#     "germany": "DE",
#     "france": "FR",
#     "italy": "IT",
#     "spain": "ES",
# }


# # Preferred main airport for country-level search
# COUNTRY_MAIN_AIRPORT = {
#     "BD": "DAC",
#     "IN": "DEL",
#     "JP": "NRT",
#     "US": "JFK",
#     "GB": "LHR",
#     "AE": "DXB",
#     "SG": "SIN",
#     "MY": "KUL",
#     "TH": "BKK",
#     "ID": "CGK",
#     "CN": "PEK",
#     "KR": "ICN",
#     "NP": "KTM",
#     "QA": "DOH",
#     "SA": "JED",
#     "TR": "IST",
#     "CA": "YYZ",
#     "AU": "SYD",
#     "DE": "FRA",
#     "FR": "CDG",
#     "IT": "FCO",
#     "ES": "MAD",
# }




# CITY_MAIN_AIRPORT = {
#     "dhaka": "DAC",
#     "delhi": "DEL",
#     "new delhi": "DEL",
#     "mumbai": "BOM",
#     "kolkata": "CCU",
#     "chennai": "MAA",
#     "bangalore": "BLR",
#     "bengaluru": "BLR",
#     "tokyo": "NRT",
#     "osaka": "KIX",
#     "kyoto": "KIX",
#     "new york": "JFK",
#     "london": "LHR",
#     "dubai": "DXB",
#     "singapore": "SIN",
#     "kuala lumpur": "KUL",
#     "bangkok": "BKK",
#     "doha": "DOH",
#     "istanbul": "IST",
#     "toronto": "YYZ",
#     "sydney": "SYD",
#     "paris": "CDG",
#     "rome": "FCO",
#     "madrid": "MAD",
#     "frankfurt": "FRA",
# }


# def clean_text(text: str) -> str:
#     text = text.lower().strip()
#     text = re.sub(r"[^a-z0-9\s]", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     stop_words = [
#         "flight", "flights", "ticket", "tickets", "trip", "travel",
#         "plan", "complete", "days", "day", "including", "hotel",
#         "hotels", "sightseeing", "under", "budget", "info", "information"
#     ]
#     words = [w for w in text.split() if w not in stop_words]
#     return " ".join(words).strip()



# def country_name_to_code(text: str):
#     text = clean_text(text)

#     if text in COUNTRY_ALIASES:
#         return COUNTRY_ALIASES[text]

#     try:
#         country = pycountry.countries.lookup(text)
#         return country.alpha_2
#     except LookupError:
#         pass

#     # Detect country name inside longer text
#     for country in pycountry.countries:
#         country_name = country.name.lower()
#         if country_name in text:
#             return country.alpha_2

#     for alias, code in COUNTRY_ALIASES.items():
#         if alias in text:
#             return code

#     return None



# def airport_country_matches(airport: dict, country_code: str) -> bool:
#     airport_country = str(airport.get("country", "")).upper().strip()

#     if airport_country == country_code:
#         return True

#     try:
#         country = pycountry.countries.get(alpha_2=country_code)
#         if country and airport_country.lower() == country.name.lower():
#             return True
#     except Exception:
#         pass

#     return False




# def get_best_airport_for_country(country_code: str):
#     preferred = COUNTRY_MAIN_AIRPORT.get(country_code)

#     if preferred and preferred in AIRPORTS:
#         return preferred

#     candidates = []

#     for iata, airport in AIRPORTS.items():
#         if not iata:
#             continue

#         if airport_country_matches(airport, country_code):
#             name = str(airport.get("name", "")).lower()
#             city = str(airport.get("city", "")).lower()

#             score = 0

#             if "international" in name:
#                 score += 50
#             if "intl" in name:
#                 score += 40
#             if "capital" in name:
#                 score += 20
#             if city:
#                 score += 5

#             candidates.append((score, iata))

#     if not candidates:
#         return None

#     candidates.sort(reverse=True)
#     return candidates[0][1]




# def resolve_location_to_iata(location: str):
#     """
#     Converts country/city/airport/IATA into IATA code.

#     Examples:
#     Bangladesh -> DAC
#     Japan -> NRT
#     Dhaka -> DAC
#     Tokyo -> NRT
#     DAC -> DAC
#     """

#     if not location:
#         return None

#     raw_location = location.strip()

#     # Direct IATA code
#     if re.fullmatch(r"[A-Za-z]{3}", raw_location):
#         code = raw_location.upper()
#         if code in AIRPORTS:
#             return code

#     location_clean = clean_text(raw_location)

#     if not location_clean:
#         return None

#     # City preferred airport
#     if location_clean in CITY_MAIN_AIRPORT:
#         return CITY_MAIN_AIRPORT[location_clean]

#     # Country preferred airport
#     country_code = country_name_to_code(location_clean)
#     if country_code:
#         airport = get_best_airport_for_country(country_code)
#         if airport:
#             return airport

#     # Exact city match from airport database
#     city_matches = []

#     for iata, airport in AIRPORTS.items():
#         city = str(airport.get("city", "")).lower().strip()
#         name = str(airport.get("name", "")).lower().strip()

#         score = 0

#         if city == location_clean:
#             score += 100
#         elif location_clean in city:
#             score += 70

#         if location_clean in name:
#             score += 50

#         if "international" in name:
#             score += 10

#         if score > 0:
#             city_matches.append((score, iata))

#     if city_matches:
#         city_matches.sort(reverse=True)
#         return city_matches[0][1]

#     return None




# def find_location_mentions(query: str):
#     """
#     Finds country or city names inside a natural language query.
#     """

#     q = query.lower()
#     mentions = []

#     # Country aliases
#     for alias in COUNTRY_ALIASES:
#         if re.search(rf"\b{re.escape(alias)}\b", q):
#             mentions.append(alias)

#     # Country names from pycountry
#     for country in pycountry.countries:
#         name = country.name.lower()
#         if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b", q):
#             mentions.append(name)

#     # City names from our preferred city map
#     for city in CITY_MAIN_AIRPORT:
#         if re.search(rf"\b{re.escape(city)}\b", q):
#             mentions.append(city)

#     # Remove duplicate while keeping order
#     unique_mentions = []
#     for item in mentions:
#         if item not in unique_mentions:
#             unique_mentions.append(item)

#     return unique_mentions


# def parse_route(query: str):
#     """
#     Returns:
#     dep_iata, arr_iata

#     Can return:
#     None, None  -> global live flights
#     DAC, NRT    -> filtered route
#     DAC, None   -> all flights from DAC
#     None, NRT   -> all flights to NRT
#     """

#     q = query.strip()
#     q_lower = q.lower()

#     # Global / all-country query
#     global_keywords = [
#         "all country",
#         "all countries",
#         "global flight",
#         "global flights",
#         "all flight",
#         "all flights",
#         "worldwide flight",
#         "worldwide flights",
#     ]

#     if any(keyword in q_lower for keyword in global_keywords):
#         return None, None

#     # Direct IATA code route: DAC to NRT
#     codes = re.findall(r"\b[A-Z]{3}\b", q)

#     if len(codes) >= 2:
#         dep = codes[0].upper()
#         arr = codes[1].upper()
#         return dep, arr

#     # Pattern: from X to Y
#     match = re.search(
#         r"\bfrom\s+(.+?)\s+\bto\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
#         q_lower,
#     )

#     if match:
#         origin_text = match.group(1)
#         dest_text = match.group(2)

#         dep_iata = resolve_location_to_iata(origin_text)
#         arr_iata = resolve_location_to_iata(dest_text)

#         return dep_iata, arr_iata

#     # Pattern: to Y from X
#     match = re.search(
#         r"\bto\s+(.+?)\s+\bfrom\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
#         q_lower,
#     )

#     if match:
#         dest_text = match.group(1)
#         origin_text = match.group(2)

#         dep_iata = resolve_location_to_iata(origin_text)
#         arr_iata = resolve_location_to_iata(dest_text)

#         return dep_iata, arr_iata

#     # Pattern: flights from X
#     match = re.search(r"\bfrom\s+(.+?)(?:[.!?]|$)", q_lower)

#     if match:
#         origin_text = match.group(1)
#         dep_iata = resolve_location_to_iata(origin_text)
#         return dep_iata, None

#     # Pattern: flights to X
#     match = re.search(r"\bto\s+(.+?)(?:[.!?]|$)", q_lower)

#     if match:
#         dest_text = match.group(1)
#         arr_iata = resolve_location_to_iata(dest_text)
#         return None, arr_iata

#     # Fallback: find country/city mentions
#     mentions = find_location_mentions(q)

#     if len(mentions) >= 2:
#         dep_iata = resolve_location_to_iata(mentions[0])
#         arr_iata = resolve_location_to_iata(mentions[1])
#         return dep_iata, arr_iata

#     if len(mentions) == 1:
#         arr_iata = resolve_location_to_iata(mentions[0])
#         return DEFAULT_ORIGIN_IATA, arr_iata

#     return None, None


# def format_flight(flight: dict):
#     airline = flight.get("airline", {}).get("name") or "Unknown airline"
#     flight_number = flight.get("flight", {}).get("iata") or "Unknown flight number"
#     status = flight.get("flight_status") or "Unknown"

#     dep = flight.get("departure", {}) or {}
#     arr = flight.get("arrival", {}) or {}

#     dep_airport = dep.get("airport") or "Unknown departure airport"
#     dep_iata = dep.get("iata") or "Unknown"
#     dep_terminal = dep.get("terminal") or "N/A"
#     dep_gate = dep.get("gate") or "N/A"
#     dep_scheduled = dep.get("scheduled") or "Unknown"
#     dep_delay = dep.get("delay")
#     dep_delay_text = f"{dep_delay} minutes" if dep_delay is not None else "N/A"

#     arr_airport = arr.get("airport") or "Unknown arrival airport"
#     arr_iata = arr.get("iata") or "Unknown"
#     arr_terminal = arr.get("terminal") or "N/A"
#     arr_gate = arr.get("gate") or "N/A"
#     arr_scheduled = arr.get("scheduled") or "Unknown"
#     arr_delay = arr.get("delay")
#     arr_delay_text = f"{arr_delay} minutes" if arr_delay is not None else "N/A"

#     return f"""
# Airline: {airline}
# Flight: {flight_number}
# Status: {status}

# Departure:
# - Airport: {dep_airport}
# - IATA: {dep_iata}
# - Terminal: {dep_terminal}
# - Gate: {dep_gate}
# - Scheduled: {dep_scheduled}
# - Delay: {dep_delay_text}

# Arrival:
# - Airport: {arr_airport}
# - IATA: {arr_iata}
# - Terminal: {arr_terminal}
# - Gate: {arr_gate}
# - Scheduled: {arr_scheduled}
# - Delay: {arr_delay_text}
# """.strip()


# def search_flights(query: str, limit: int = 10):
#     if not API_KEY:
#         return (
#             "Flight API error: AVIATIONSTACK_API_KEY is missing.\n"
#             "Please add this in your .env file:\n"
#             "AVIATIONSTACK_API_KEY=your_api_key_here"
#         )

#     dep_iata, arr_iata = parse_route(query)

#     params = {
#         "access_key": API_KEY,
#         "limit": min(limit, 100),
#     }

#     if dep_iata:
#         params["dep_iata"] = dep_iata

#     if arr_iata:
#         params["arr_iata"] = arr_iata

#     try:
#         response = requests.get(BASE_URL, params=params, timeout=30)
#         data = response.json()
#     except requests.exceptions.RequestException as e:
#         return f"Flight API request failed: {e}"
#     except ValueError:
#         return "Flight API returned invalid JSON."

#     if "error" in data:
#         error = data["error"]
#         return (
#             "Flight API error:\n"
#             f"Code: {error.get('code', 'Unknown')}\n"
#             f"Message: {error.get('message', 'Unknown error')}"
#         )

#     flight_data = data.get("data", [])

#     if not flight_data:
#         route_text = ""

#         if dep_iata and arr_iata:
#             route_text = f" for route {dep_iata} to {arr_iata}"
#         elif dep_iata:
#             route_text = f" from {dep_iata}"
#         elif arr_iata:
#             route_text = f" to {arr_iata}"

#         return (
#             f"No live flight data found{route_text}.\n\n"
#             "Note: AviationStack provides live/status flight data, not ticket prices. "
#             "For actual fare prices, use a flight-pricing API such as Amadeus."
#         )

#     route_info = "Global live flights"

#     if dep_iata and arr_iata:
#         route_info = f"Live flights from {dep_iata} to {arr_iata}"
#     elif dep_iata:
#         route_info = f"Live flights from {dep_iata}"
#     elif arr_iata:
#         route_info = f"Live flights to {arr_iata}"

#     formatted_flights = [format_flight(flight) for flight in flight_data[:limit]]

#     return f"{route_info}\n\n" + "\n\n---\n\n".join(formatted_flights)


# if __name__ == "__main__":
#     print(search_flights("Plan a 7 days Japan trip from Bangladesh"))
#     print("\n" + "=" * 80 + "\n")
#     print(search_flights("all country flight info"))

import os
import re
from datetime import datetime

import certifi
import airportsdata
import pycountry
import requests
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "DEL")

SERPAPI_URL = "https://serpapi.com/search.json"

AIRPORTS = airportsdata.load("IATA")


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:
    """
    Cleans user query/location text.
    """

    if not text:
        return ""

    text = text.lower().strip()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    stop_words = {
        "flight",
        "flights",
        "ticket",
        "tickets",
        "trip",
        "travel",
        "plan",
        "complete",
        "days",
        "day",
        "including",
        "hotel",
        "hotels",
        "sightseeing",
        "under",
        "budget",
        "info",
        "information",
        "from",
        "to",
    }

    words = [
        word
        for word in text.split()
        if word not in stop_words
    ]

    return " ".join(words).strip()


# ============================================================
# COUNTRY RESOLUTION
# ============================================================

def country_name_to_code(text: str):
    """
    Converts country name into ISO alpha-2 code.

    Example:
        India -> IN
        Japan -> JP
        Germany -> DE
    """

    if not text:
        return None

    text = clean_text(text)

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2

    except LookupError:
        pass

    # Search country names inside longer text
    for country in pycountry.countries:

        country_name = country.name.lower()

        if len(country_name) >= 4:

            if re.search(
                rf"\b{re.escape(country_name)}\b",
                text
            ):
                return country.alpha_2

    return None


# ============================================================
# AIRPORT COUNTRY CHECK
# ============================================================

def airport_country_matches(
    airport: dict,
    country_code: str
) -> bool:

    airport_country = str(
        airport.get("country", "")
    ).upper().strip()

    if airport_country == country_code:
        return True

    try:

        country = pycountry.countries.get(
            alpha_2=country_code
        )

        if country:

            if airport_country.lower() == country.name.lower():
                return True

    except Exception:
        pass

    return False


# ============================================================
# DYNAMIC COUNTRY → AIRPORT
# ============================================================

def get_best_airport_for_country(country_code: str):
    """
    Dynamically finds an airport for a country.

    No manually maintained country → airport dictionary.
    """

    candidates = []

    for iata, airport in AIRPORTS.items():

        if not iata:
            continue

        if not airport_country_matches(
            airport,
            country_code
        ):
            continue

        name = str(
            airport.get("name", "")
        ).lower()

        city = str(
            airport.get("city", "")
        ).lower()

        score = 0

        # Prefer international airports
        if "international" in name:
            score += 50

        if "intl" in name:
            score += 40

        # Prefer airports associated with a city
        if city:
            score += 10

        candidates.append(
            (score, iata)
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return candidates[0][1]


# ============================================================
# LOCATION → IATA
# ============================================================

def resolve_location_to_iata(location: str):
    """
    Converts:

        IATA code
        city
        country

    into an airport IATA code.

    Examples:

        DEL -> DEL
        Delhi -> DEL
        Tokyo -> NRT
        Japan -> dynamically selected airport
    """

    if not location:
        return None

    raw_location = location.strip()

    # --------------------------------------------------------
    # Direct IATA code
    # --------------------------------------------------------

    if re.fullmatch(
        r"[A-Za-z]{3}",
        raw_location
    ):

        code = raw_location.upper()

        if code in AIRPORTS:
            return code

    location_clean = clean_text(
        raw_location
    )

    if not location_clean:
        return None

    # --------------------------------------------------------
    # Country
    # --------------------------------------------------------

    country_code = country_name_to_code(
        location_clean
    )

    if country_code:

        airport = get_best_airport_for_country(
            country_code
        )

        if airport:
            return airport

    # --------------------------------------------------------
    # Dynamic city search
    # --------------------------------------------------------

    city_matches = []

    for iata, airport in AIRPORTS.items():

        city = str(
            airport.get("city", "")
        ).lower().strip()

        name = str(
            airport.get("name", "")
        ).lower().strip()

        score = 0

        # Exact city match
        if city == location_clean:
            score += 100

        # Partial city match
        elif location_clean in city:
            score += 70

        # Airport name match
        if location_clean in name:
            score += 50

        # Prefer international airport
        if "international" in name:
            score += 20

        if score > 0:

            city_matches.append(
                (score, iata)
            )

    if city_matches:

        city_matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return city_matches[0][1]

    return None


# ============================================================
# FIND LOCATIONS IN NATURAL LANGUAGE
# ============================================================

def find_location_mentions(query: str):
    """
    Finds country/city names from the airport database
    and pycountry.
    """

    if not query:
        return []

    q = query.lower()

    mentions = []

    # --------------------------------------------------------
    # Countries from pycountry
    # --------------------------------------------------------

    for country in pycountry.countries:

        name = country.name.lower()

        if len(name) >= 4:

            if re.search(
                rf"\b{re.escape(name)}\b",
                q
            ):

                mentions.append(name)

    # --------------------------------------------------------
    # Cities from airportsdata
    # --------------------------------------------------------

    cities = set()

    for airport in AIRPORTS.values():

        city = str(
            airport.get("city", "")
        ).lower().strip()

        if city and len(city) >= 3:
            cities.add(city)

    # Longest cities first
    cities = sorted(
        cities,
        key=len,
        reverse=True
    )

    for city in cities:

        if re.search(
            rf"\b{re.escape(city)}\b",
            q
        ):

            mentions.append(city)

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    unique_mentions = []

    for item in mentions:

        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions


# ============================================================
# DATE EXTRACTION
# ============================================================

def extract_date(query: str):
    """
    Attempts to find a travel date in the user's query.

    Supported examples:

        October 10 2026
        Oct 10 2026
        10 October 2026
        2026-10-10
    """

    if not query:
        return None

    patterns = [
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",

        r"\b(?:jan|january|feb|february|mar|march|"
        r"apr|april|may|jun|june|jul|july|aug|august|"
        r"sep|september|oct|october|nov|november|"
        r"dec|december)"
        r"\s+\d{1,2}(?:st|nd|rd|th)?"
        r"(?:\s+\d{4})?\b",

        r"\b\d{1,2}\s+"
        r"(?:jan|january|feb|february|mar|march|"
        r"apr|april|may|jun|june|jul|july|aug|august|"
        r"sep|september|oct|october|nov|november|"
        r"dec|december)"
        r"(?:\s+\d{4})?\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query,
            re.IGNORECASE
        )

        if not match:
            continue

        date_text = match.group(0)

        formats = [
            "%Y-%m-%d",
            "%B %d %Y",
            "%b %d %Y",
            "%d %B %Y",
            "%d %b %Y",
        ]

        for fmt in formats:

            try:

                parsed = datetime.strptime(
                    re.sub(
                        r"(st|nd|rd|th)",
                        "",
                        date_text,
                        flags=re.IGNORECASE
                    ),
                    fmt
                )

                return parsed.strftime(
                    "%Y-%m-%d"
                )

            except ValueError:
                continue

    return None


# ============================================================
# ROUTE PARSER
# ============================================================

def parse_route(query: str):
    """
    Returns:

        dep_iata, arr_iata

    Examples:

        "flights from Delhi to Tokyo"
            -> DEL, NRT

        "flights to Japan"
            -> DEL, dynamically resolved Japan airport

        "flights from Delhi"
            -> DEL, None
    """

    q = query.strip()

    q_lower = q.lower()

    # --------------------------------------------------------
    # Direct IATA route
    # --------------------------------------------------------

    codes = re.findall(
        r"\b[A-Z]{3}\b",
        q
    )

    valid_codes = [
        code.upper()
        for code in codes
        if code.upper() in AIRPORTS
    ]

    if len(valid_codes) >= 2:

        return (
            valid_codes[0],
            valid_codes[1]
        )

    # --------------------------------------------------------
    # FROM X TO Y
    # --------------------------------------------------------

    match = re.search(
        r"\bfrom\s+(.+?)\s+to\s+(.+?)(?:"
        r"\s+on\b|"
        r"\s+for\b|"
        r"\s+under\b|"
        r"\s+including\b|"
        r"\s+with\b|"
        r"\s+in\b|"
        r"\s+at\b|"
        r"[.!?]|"
        r"$)",
        q_lower
    )

    if match:

        origin_text = match.group(1)

        destination_text = match.group(2)

        dep_iata = resolve_location_to_iata(
            origin_text
        )

        arr_iata = resolve_location_to_iata(
            destination_text
        )

        return dep_iata, arr_iata

    # --------------------------------------------------------
    # TO Y FROM X
    # --------------------------------------------------------

    match = re.search(
        r"\bto\s+(.+?)\s+from\s+(.+?)(?:"
        r"\s+on\b|"
        r"\s+for\b|"
        r"\s+under\b|"
        r"\s+including\b|"
        r"\s+with\b|"
        r"\s+in\b|"
        r"\s+at\b|"
        r"[.!?]|"
        r"$)",
        q_lower
    )

    if match:

        destination_text = match.group(1)

        origin_text = match.group(2)

        dep_iata = resolve_location_to_iata(
            origin_text
        )

        arr_iata = resolve_location_to_iata(
            destination_text
        )

        return dep_iata, arr_iata

    # --------------------------------------------------------
    # FROM X
    # --------------------------------------------------------

    match = re.search(
        r"\bfrom\s+(.+?)(?:[.!?]|$)",
        q_lower
    )

    if match:

        origin_text = match.group(1)

        dep_iata = resolve_location_to_iata(
            origin_text
        )

        return dep_iata, None

    # --------------------------------------------------------
    # TO X
    # --------------------------------------------------------

    match = re.search(
        r"\bto\s+(.+?)(?:[.!?]|$)",
        q_lower
    )

    if match:

        destination_text = match.group(1)

        arr_iata = resolve_location_to_iata(
            destination_text
        )

        return None, arr_iata

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    mentions = find_location_mentions(
        q
    )

    if len(mentions) >= 2:

        dep_iata = resolve_location_to_iata(
            mentions[0]
        )

        arr_iata = resolve_location_to_iata(
            mentions[1]
        )

        return dep_iata, arr_iata

    if len(mentions) == 1:

        arr_iata = resolve_location_to_iata(
            mentions[0]
        )

        return (
            DEFAULT_ORIGIN_IATA,
            arr_iata
        )

    return None, None


# ============================================================
# SERPAPI FLIGHT FORMATTER
# ============================================================

def format_flight(flight: dict):
    """
    Converts SerpAPI Google Flights result
    into readable text.
    """

    airline = flight.get(
        "airline",
        "Unknown airline"
    )

    flight_number = flight.get(
        "flight_number",
        "Unknown flight"
    )

    duration = flight.get(
        "duration",
        "Unknown"
    )

    stops = flight.get(
        "stops",
        0
    )

    price = flight.get(
        "price",
        "Unknown"
    )

    departure = flight.get(
        "departure_airport",
        {}
    )

    arrival = flight.get(
        "arrival_airport",
        {}
    )

    dep_name = departure.get(
        "name",
        "Unknown"
    )

    dep_code = departure.get(
        "id",
        "Unknown"
    )

    dep_time = departure.get(
        "time",
        "Unknown"
    )

    arr_name = arrival.get(
        "name",
        "Unknown"
    )

    arr_code = arrival.get(
        "id",
        "Unknown"
    )

    arr_time = arrival.get(
        "time",
        "Unknown"
    )

    stop_text = (
        "Non-stop"
        if stops == 0
        else f"{stops} stop(s)"
    )

    return f"""
Airline: {airline}
Flight: {flight_number}
Price: {price}
Duration: {duration}
Stops: {stop_text}

Departure:
- Airport: {dep_name}
- IATA: {dep_code}
- Time: {dep_time}

Arrival:
- Airport: {arr_name}
- IATA: {arr_code}
- Time: {arr_time}
""".strip()


# ============================================================
# SERPAPI GOOGLE FLIGHTS SEARCH
# ============================================================

def search_flights(
    query: str,
    limit: int = 10
):
    """
    Searches Google Flights through SerpAPI.
    """

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    if not SERPAPI_API_KEY:

        return (
            "Flight API error: "
            "SERPAPI_API_KEY is missing.\n\n"
            "Add this to your .env file:\n\n"
            "SERPAPI_API_KEY=your_serpapi_key"
        )

    # --------------------------------------------------------
    # ROUTE
    # --------------------------------------------------------

    dep_iata, arr_iata = parse_route(
        query
    )

    if not dep_iata:

        return (
            "I could not determine the "
            "departure airport."
        )

    if not arr_iata:

        return (
            "I could not determine the "
            "destination airport."
        )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    outbound_date = extract_date(
        query
    )

    if not outbound_date:

        return (
            f"I found the route "
            f"{dep_iata} → {arr_iata}, "
            "but I need a departure date "
            "to search Google Flights.\n\n"
            "Example:\n"
            "Find flights from Delhi to Tokyo "
            "on October 20 2026."
        )

    # --------------------------------------------------------
    # SERPAPI PARAMETERS
    # --------------------------------------------------------

    params = {
    "engine": "google_flights",
    "api_key": SERPAPI_API_KEY,

    "departure_id": dep_iata,
    "arrival_id": arr_iata,

    "outbound_date": outbound_date,

    # 2 = one-way
    "type": "2",

    "currency": "INR",
    "hl": "en",
    "gl": "in",
}

    # --------------------------------------------------------
    # API REQUEST
    # --------------------------------------------------------

    try:

        response = requests.get(
            SERPAPI_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:

        return (
            f"Flight API request failed: {e}"
        )

    except ValueError:

        return (
            "SerpAPI returned invalid JSON."
        )

    # --------------------------------------------------------
    # SERPAPI ERROR
    # --------------------------------------------------------

    if "error" in data:

        return (
            "Flight API error:\n"
            f"{data['error']}"
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    flights = data.get(
        "best_flights",
        []
    )

    if not flights:

        flights = data.get(
            "other_flights",
            []
        )

    if not flights:

        return (
            f"No flights found for "
            f"{dep_iata} → {arr_iata} "
            f"on {outbound_date}."
        )

    # --------------------------------------------------------
    # LIMIT RESULTS
    # --------------------------------------------------------

    flights = flights[:limit]

    formatted_results = []

    for flight_group in flights:

        # SerpAPI Google Flights returns
        # itinerary groups containing flights.

        segments = flight_group.get(
            "flights",
            []
        )

        if not segments:
            continue

        # First segment
        first_segment = segments[0]

        # Last segment
        last_segment = segments[-1]

        # Build a readable result
        result = {
            "airline": first_segment.get(
                "airline",
                "Unknown airline"
            ),

            "flight_number": first_segment.get(
                "flight_number",
                "Unknown"
            ),

            "duration": flight_group.get(
                "total_duration",
                "Unknown"
            ),

            "stops": len(segments) - 1,

            "price": flight_group.get(
                "price",
                "Unknown"
            ),

            "departure_airport": first_segment.get(
                "departure_airport",
                {}
            ),

            "arrival_airport": last_segment.get(
                "arrival_airport",
                {}
            ),
        }

        formatted_results.append(
            format_flight(result)
        )

    if not formatted_results:

        return (
            "Flights were returned by SerpAPI, "
            "but they could not be formatted."
        )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    route_info = (
        f"Flight options: "
        f"{dep_iata} → {arr_iata}\n"
        f"Departure date: {outbound_date}"
    )

    return (
        route_info
        + "\n\n"
        + "\n\n---\n\n".join(
            formatted_results
        )
    )

