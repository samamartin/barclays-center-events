#!/usr/bin/env python3
"""
Barclays Center weekly events newsletter.

Usage:
  python main.py              # Fetch events and send to the Google Group
  python main.py --preview    # Save newsletter_preview.html instead of sending
  python main.py --list       # Print upcoming events to stdout

Cron (every Monday at 8 AM):
  0 8 * * 1 cd /path/to/barclays-boulevardier && python main.py >> newsletter.log 2>&1
"""
import sys
from datetime import datetime

from config import TICKETMASTER_API_KEY, SMTP_USER, GOOGLE_GROUP_EMAIL, DAYS_AHEAD
from scraper import fetch_events
from newsletter import build_html
from mailer import send_newsletter


def validate_config(send_mode):
    errors = []
    if not TICKETMASTER_API_KEY:
        errors.append("TICKETMASTER_API_KEY is not set")
    if send_mode and not SMTP_USER:
        errors.append("SMTP_USER is not set")
    if send_mode and not GOOGLE_GROUP_EMAIL:
        errors.append("GOOGLE_GROUP_EMAIL is not set")
    return errors


def main():
    preview = "--preview" in sys.argv
    list_only = "--list" in sys.argv
    send_mode = not preview and not list_only

    errors = validate_config(send_mode)
    if errors:
        print("Configuration errors:")
        for e in errors:
            print(f"  - {e}")
        print("\nCopy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    print(f"Fetching events for the next {DAYS_AHEAD} days...")
    try:
        events = fetch_events()
    except Exception as exc:
        print(f"Failed to fetch events: {exc}")
        sys.exit(1)

    print(f"Found {len(events)} event(s).")

    if list_only:
        for e in events:
            time_part = f" at {e['time']}" if e["time"] else ""
            print(f"  {e['date']}{time_part}  |  {e['name']}")
        return

    html = build_html(events)

    if preview:
        path = "newsletter_preview.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Preview saved to {path}  (open in a browser to inspect)")
        return

    today = datetime.now()
    subject = f"Barclays Boulevardier: {len(events)} Upcoming Events — {today.strftime('%B %-d, %Y')}"
    print(f"Sending to {GOOGLE_GROUP_EMAIL}...")
    send_newsletter(html, subject)
    print("Done.")


if __name__ == "__main__":
    main()
