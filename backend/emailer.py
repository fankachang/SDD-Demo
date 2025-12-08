import os
import smtplib
from email.message import EmailMessage
from typing import List, Dict
from jinja2 import Template
import socket


def render_template(subject: str, body_template: str, context: Dict) -> Dict:
    subject_rendered = Template(subject).render(**context)
    body_rendered = Template(body_template).render(**context)
    return {"subject": subject_rendered, "body": body_rendered}


def send_synchronously(subject: str, body: str, recipients: List[Dict]) -> List[Dict]:
    """Send emails synchronously via SMTP. Returns list of per-recipient results.

    If SMTP configuration is absent, simulate success for local testing.
    """
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "0") or 0)
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    timeout = int(os.getenv("SMTP_TIMEOUT", "30"))

    results = []

    # If no SMTP host configured, simulate success (useful for dev)
    if not host:
        for r in recipients:
            results.append({"email": r["email"], "result": "success", "detail": "simulated"})
        return results

    try:
        with smtplib.SMTP(host, port, timeout=timeout) as smtp:
            smtp.ehlo()
            if port == 587:
                smtp.starttls()
                smtp.ehlo()
            if user and password:
                smtp.login(user, password)

            for r in recipients:
                msg = EmailMessage()
                msg["From"] = user or f"no-reply@{host}"
                msg["To"] = r["email"]
                msg["Subject"] = subject
                msg.set_content(body)
                try:
                    smtp.send_message(msg)
                    results.append({"email": r["email"], "result": "success", "detail": "sent"})
                except (smtplib.SMTPException, socket.error) as e:
                    results.append({"email": r["email"], "result": "failure", "detail": str(e)})
    except (smtplib.SMTPException, socket.error) as e:
        # Entire session failed (treat as timeout/failure for all)
        for r in recipients:
            results.append({"email": r["email"], "result": "failure", "detail": f"session error: {e}"})

    return results
