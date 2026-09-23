import os
import logging
import requests
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

# Must match a verified sender in your Brevo account (Senders, Domains & Dedicated IPs > Senders)
MAIL_FROM = os.getenv("MAIL_FROM", "cpms.project1@gmail.com")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "CPMS")


async def _send_email(to_email: str, subject: str, html: str):
    if not BREVO_API_KEY:
        logging.error("BREVO_API_KEY is not set — skipping email send.")
        return

    payload = {
        "sender": {"name": MAIL_FROM_NAME, "email": MAIL_FROM},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html,
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    try:
        response = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=10)
        if response.status_code >= 400:
            logging.error(f"Brevo send failed ({response.status_code}): {response.text}")
            response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to send email via Brevo: {e}")
        raise


async def visit_requested_email(email: EmailStr, visitor_name: str, inmate_name: str, visit_date: str, prison_name: str):
    html = f"""
    <p>Dear {visitor_name},</p>
    <p>Thank you for submitting a request to visit inmate <strong>{inmate_name}</strong>.</p>
    <p>Your visit request for <strong>{visit_date}</strong> has been received and is currently pending approval. We will notify you once a decision has been made.</p>
    <p>If you have any questions, please contact us.</p>
    <br>
    <p>Best regards,</p>
    <p>{prison_name} Administration</p>
    """
    await _send_email(email, "Visit Requested Successfully", html)


async def visit_confirmed_email(email: EmailStr, visitor_name: str, inmate_name: str, visit_date: str, visit_time: str, prison_name: str):
    html = f"""
    <p>Dear {visitor_name},</p>
    <p>We are pleased to inform you that your request to visit inmate <strong>{inmate_name}</strong> has been approved.</p>
    <p><strong>Visit Details:</strong></p>
    <ul>
        <li><strong>Date:</strong> {visit_date}</li>
        <li><strong>Time:</strong> {visit_time}</li>
        <li><strong>Location:</strong> {prison_name}</li>
    </ul>
    <p>Please make sure to arrive at least 15 minutes before your scheduled time and bring a valid ID for verification.</p>
    <p>Kindly follow all facility rules and regulations during your visit.</p>
    <p>If you have any questions or need to reschedule, please contact us.</p>
    <br>
    <p>Best regards,</p>
    <p>{prison_name} Administration</p>
    """
    await _send_email(email, "Visit Confirmed", html)


async def visit_rejected_email(email: EmailStr, visitor_name: str, inmate_name: str, prison_name: str, reason: str = ""):
    reason_html = f"<p><strong>Reason:</strong> {reason}</p>" if reason else ""
    html = f"""
    <p>Dear {visitor_name},</p>
    <p>Thank you for your request to visit inmate <strong>{inmate_name}</strong>.</p>
    <p>We regret to inform you that your visit request has been declined.</p>
    {reason_html}
    <p>You may submit a new request for a different date or contact the administration for further clarification.</p>
    <p>We appreciate your understanding.</p>
    <br>
    <p>Best regards,</p>
    <p>{prison_name} Administration</p>
    """
    await _send_email(email, "Visit Rejected", html)
