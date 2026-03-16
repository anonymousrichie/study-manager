from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def send_notification(to_email: str | None, subject: str, message: str) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")

    if not smtp_host or not smtp_username or not smtp_password or not smtp_from or not to_email:
        print(f"[Reminder] {subject} - {message}")
        return

    email = EmailMessage()
    email["From"] = smtp_from
    email["To"] = to_email
    email["Subject"] = subject
    email.set_content(message)

    port = int(os.getenv("SMTP_PORT", "587"))
    with smtplib.SMTP(smtp_host, port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(email)
