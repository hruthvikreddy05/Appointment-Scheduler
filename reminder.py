import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from database import SessionLocal
import models

# Load environment variables from .env
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_email_notification(to_email: str, name: str, date_str: str, time_str: str, reason: str):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("❌ Email credentials missing in .env file.")
        return False

    subject = "⏰ Reminder: Upcoming Appointment in 6 Hours"
    body = f"""Hello {name},

This is an automated reminder that your appointment is scheduled in less than 6 hours!

Appointment Details:
- Date: {date_str}
- Time: {time_str}
- Reason: {reason}

Thank you!
"""

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"✅ Reminder email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def check_and_send_6hr_reminders():
    db = SessionLocal()
    try:
        now = datetime.now()
        target_window_start = now
        target_window_end = now + timedelta(hours=6)

        pending_appointments = db.query(models.AppointmentDB).filter(
            models.AppointmentDB.reminder_sent == 0
        ).all()

        for app in pending_appointments:
            try:
                app_datetime = datetime.strptime(f"{app.date} {app.time}", "%Y-%m-%d %H:%M")

                if target_window_start <= app_datetime <= target_window_end:
                    if send_email_notification(app.email, app.name, app.date, app.time, app.reason):
                        app.reminder_sent = 1
                        db.commit()
            except ValueError:
                continue
    finally:
        db.close()
