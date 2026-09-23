import os
import logging
import resend
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY", "")

# Use Resend's default testing sender if you haven't verified your own domain yet.
# Once you verify a domain in Resend, change this to something like "no-reply@yourdomain.com"
MAIL_FROM = os.getenv("MAIL_FROM", "onboarding@resend.dev")


async def _send_email(to_email: str, subject: str, html: str):
    if not resend.api_key:
        logging.error("RESEND_API_KEY is not set — skipping email send.")
        return

    try:
        resend.Emails.send({
            "from": MAIL_FROM,
            "to": [to_email],
            "subject": subject,
            "html": html,
        })
    except Exception as e:
        logging.error(f"Failed to send email via Resend: {e}")
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
