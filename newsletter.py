from datetime import datetime, timedelta
from config import DAYS_AHEAD


def build_html(events):
    today = datetime.now()
    end = today + timedelta(days=DAYS_AHEAD)
    date_range = f"{today.strftime('%B %-d')} – {end.strftime('%B %-d, %Y')}"
    count_label = f"{len(events)} event{'s' if len(events) != 1 else ''}"

    if events:
        events_html = "\n".join(_event_card(e) for e in events)
    else:
        events_html = (
            '<p style="text-align:center;color:#666;font-size:16px;padding:40px 0;">'
            f"No events scheduled in the next {DAYS_AHEAD} days. Check back next week!"
            "</p>"
        )

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Barclays Center Events</title>
</head>
<body style="margin:0;padding:0;background:#EDF2F7;font-family:'Helvetica Neue',Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="background:#2C5282;padding:32px 24px;text-align:center;">
      <p style="margin:0 0 4px;color:#90CDF4;font-size:11px;letter-spacing:2px;text-transform:uppercase;">
        Weekly Newsletter
      </p>
      <h1 style="margin:0;color:#fff;font-size:30px;font-weight:700;letter-spacing:1px;">
        Barclays Center
      </h1>
      <p style="margin:10px 0 0;color:#BEE3F8;font-size:13px;">
        {count_label} &bull; {date_range}
      </p>
    </td>
  </tr>
  <tr>
    <td style="padding:24px 16px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0"
             style="max-width:600px;margin:0 auto;">
        <tr><td>
          {events_html}
        </td></tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="background:#1A365D;padding:28px 24px;text-align:center;">
      <p style="margin:0;color:#90CDF4;font-size:12px;line-height:1.6;">
        Barclays Center &bull; 620 Atlantic Ave, Brooklyn, NY 11217<br>
        Sent every Monday morning. Events sourced from Ticketmaster.
      </p>
    </td>
  </tr>
</table>

</body>
</html>"""


def _event_card(event):
    img = (
        f'<img src="{event["image_url"]}" alt="" width="100%"'
        ' style="display:block;width:100%;height:200px;object-fit:cover;">'
        if event["image_url"] else ""
    )

    category_badge = (
        f'<span style="display:inline-block;background:#2C5282;color:#fff;'
        f'font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
        f'padding:3px 9px;border-radius:2px;margin-bottom:10px;">'
        f'{event["category"]}</span><br>'
        if event["category"] else ""
    )

    time_part = f" &bull; {event['time']}" if event["time"] else ""
    price_part = (
        f' &nbsp;<span style="color:#888;font-size:12px;">{event["price"]}</span>'
        if event["price"] else ""
    )

    return f"""\
<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:#fff;border-radius:6px;overflow:hidden;
              margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.10);">
  <tr><td style="line-height:0;">{img}</td></tr>
  <tr>
    <td style="padding:22px 24px;">
      {category_badge}
      <h2 style="margin:0 0 8px;font-size:20px;color:#111;line-height:1.3;font-weight:700;">
        {event["name"]}
      </h2>
      <p style="margin:0 0 18px;font-size:14px;color:#444;">
        <strong>{event["date"]}</strong>{time_part}{price_part}
      </p>
      <a href="{event["url"]}"
         style="display:inline-block;background:#2B6CB0;color:#fff;text-decoration:none;
                padding:11px 26px;border-radius:3px;font-size:13px;font-weight:700;
                letter-spacing:0.5px;">
        Get Tickets &rarr;
      </a>
    </td>
  </tr>
</table>"""
