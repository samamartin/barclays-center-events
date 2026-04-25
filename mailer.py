import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_NAME, FROM_EMAIL, SUBSCRIBERS_FILE


def load_subscribers():
    if not SUBSCRIBERS_FILE.exists():
        return []
    lines = SUBSCRIBERS_FILE.read_text().splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def send_newsletter(html_body, subject):
    subscribers = load_subscribers()
    if not subscribers:
        print("No subscribers found. Add email addresses to subscribers.txt.")
        return 0

    sent = 0
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        for recipient in subscribers:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
            msg["To"] = recipient
            msg.attach(MIMEText(html_body, "html", "utf-8"))
            server.sendmail(FROM_EMAIL, recipient, msg.as_string())
            print(f"  Sent to {recipient}")
            sent += 1

    return sent
