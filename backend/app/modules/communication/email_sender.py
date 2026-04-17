import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD
from app.utils.logger import log_error


def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Send an email via Gmail SMTP.
    Requires EMAIL_ADDRESS and EMAIL_APP_PASSWORD in .env
    """
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        return (
            "Email isn't configured yet. Add your EMAIL_ADDRESS and "
            "EMAIL_APP_PASSWORD to the .env file."
        )

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        return f"Email sent to {to_email} with subject '{subject}'."

    except Exception as e:
        log_error("send_email", e)
        return f"Failed to send email: {str(e)}"


def send_email_command(command: str) -> str:
    """
    Parse a natural language email command.
    Expected patterns:
        "send email to user@gmail.com subject Hello message Hi there"
        "email to user@gmail.com saying Hello"
    """
    command = command.lower().strip()

    # Try to extract email address
    import re
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', command)
    if not email_match:
        return (
            "I need an email address. Try: "
            "'send email to user@gmail.com subject Hello message Hi there'"
        )

    to_email = email_match.group()

    # Extract subject
    subject = "Message from FRIDAY"
    if "subject" in command:
        sub_idx = command.index("subject") + len("subject")
        rest = command[sub_idx:].strip()
        if "message" in rest:
            msg_idx = rest.index("message")
            subject = rest[:msg_idx].strip()
        elif "saying" in rest:
            msg_idx = rest.index("saying")
            subject = rest[:msg_idx].strip()
        else:
            subject = rest.strip()

    # Extract body
    body = "Sent via FRIDAY-X Assistant"
    for keyword in ["message ", "saying ", "body "]:
        if keyword in command:
            idx = command.index(keyword) + len(keyword)
            body = command[idx:].strip()
            break

    if subject:
        subject = subject.strip().title()

    return send_email(to_email, subject, body)
