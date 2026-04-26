import requests
from datetime import datetime, timezone, timedelta
from config import TICKETMASTER_API_KEY, TICKETMASTER_VENUE_ID, DAYS_AHEAD

BASE_URL = "https://app.ticketmaster.com/discovery/v2"


def get_venue_id():
    """Look up the Barclays Center venue ID from the Ticketmaster Discovery API."""
    if TICKETMASTER_VENUE_ID:
        return TICKETMASTER_VENUE_ID

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "keyword": "Barclays Center",
        "city": "Brooklyn",
        "stateCode": "NY",
        "countryCode": "US",
    }
    resp = requests.get(f"{BASE_URL}/venues.json", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    venues = data.get("_embedded", {}).get("venues", [])
    for venue in venues:
        if "barclays" in venue.get("name", "").lower():
            return venue["id"]
    raise RuntimeError("Could not find Barclays Center in the Ticketmaster venue directory.")


def fetch_events():
    """Return a list of upcoming events at Barclays Center, sorted by date."""
    venue_id = get_venue_id()

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=DAYS_AHEAD)

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "venueId": venue_id,
        "startDateTime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endDateTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "size": 50,
        "sort": "date,asc",
    }
    resp = requests.get(f"{BASE_URL}/events.json", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    raw_events = data.get("_embedded", {}).get("events", [])
    return [e for e in [_parse_event(r) for r in raw_events]
            if e["time"] and "barclays center tours" not in e["name"].lower()]


def _parse_event(raw):
    start = raw.get("dates", {}).get("start", {})
    local_date = start.get("localDate", "")
    local_time = start.get("localTime", "")
    time_tba = start.get("timeTBA", False) or start.get("noSpecificTime", False)

    classifications = raw.get("classifications", [{}])
    segment = classifications[0].get("segment", {}).get("name", "")
    genre = classifications[0].get("genre", {}).get("name", "")

    # Build a readable category label, skipping "Undefined" placeholders
    parts = [p for p in [segment, genre] if p and p.lower() != "undefined"]
    if len(parts) == 2 and parts[0] == parts[1]:
        parts = parts[:1]
    category = " / ".join(parts)

    price_ranges = raw.get("priceRanges", [])
    price = ""
    if price_ranges:
        lo = price_ranges[0].get("min")
        hi = price_ranges[0].get("max")
        if lo is not None and hi is not None:
            price = f"${lo:.0f}–${hi:.0f}"
        elif lo is not None:
            price = f"From ${lo:.0f}"

    # Prefer wide landscape images for the email header
    images = raw.get("images", [])
    image_url = _best_image(images)

    date_str = _fmt_date(local_date)
    time_str = "" if time_tba else _fmt_time(local_time)

    return {
        "name": raw.get("name", ""),
        "date": date_str,
        "date_iso": local_date,
        "time": time_str,
        "category": category,
        "price": price,
        "url": raw.get("url", "https://www.ticketmaster.com"),
        "image_url": image_url,
    }


def _best_image(images):
    if not images:
        return ""
    landscape = [i for i in images if i.get("ratio") == "16_9" and i.get("width", 0) >= 640]
    pool = landscape or images
    return max(pool, key=lambda i: i.get("width", 0)).get("url", "")


def _fmt_date(local_date):
    if not local_date:
        return ""
    try:
        dt = datetime.strptime(local_date, "%Y-%m-%d")
        return dt.strftime("%A, %B %-d")
    except ValueError:
        return local_date


def _fmt_time(local_time):
    if not local_time:
        return ""
    try:
        t = datetime.strptime(local_time, "%H:%M:%S")
        return t.strftime("%-I:%M %p")
    except ValueError:
        return local_time
