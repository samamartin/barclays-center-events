import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY", "")
TICKETMASTER_VENUE_ID = os.getenv("TICKETMASTER_VENUE_ID", "")
DAYS_AHEAD = int(os.getenv("DAYS_AHEAD", "14"))

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_NAME = os.getenv("FROM_NAME", "Barclays Center Newsletter")
FROM_EMAIL = os.getenv("FROM_EMAIL", "") or SMTP_USER

GOOGLE_GROUP_EMAIL = os.getenv("GOOGLE_GROUP_EMAIL", "")
