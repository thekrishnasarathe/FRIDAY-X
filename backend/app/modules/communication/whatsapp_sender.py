from app.utils.logger import log_error


# ─── Contact book (add your contacts here) ────────────────
CONTACTS = {
    # "name": "+91XXXXXXXXXX"  (with country code)
    # Example:
    # "mom": "+919876543210",
    # "rahul": "+919123456789",
}


def send_whatsapp(phone: str, message: str) -> str:
    """
    Send a WhatsApp message using pywhatkit.
    Phone must include country code (e.g., +919876543210).
    """
    try:
        import pywhatkit as kit
        from datetime import datetime

        now = datetime.now()
        # Send 1 minute from now
        hour = now.hour
        minute = now.minute + 2
        if minute >= 60:
            minute -= 60
            hour += 1

        kit.sendwhatmsg(phone, message, hour, minute, wait_time=15)
        return f"WhatsApp message scheduled to {phone}."

    except Exception as e:
        log_error("send_whatsapp", e)
        return f"Failed to send WhatsApp message: {str(e)}"


def send_whatsapp_command(command: str) -> str:
    """
    Parse a natural language WhatsApp command.
    Patterns:
        "send message to mom saying I'll be late"
        "send whatsapp to +919876543210 message Hello"
        "message to rahul saying how are you"
    """
    command = command.lower().strip()

    import re

    # Try to find a phone number
    phone_match = re.search(r'\+\d{10,15}', command)
    phone = phone_match.group() if phone_match else None

    # Try to find a contact name
    if not phone:
        for name, number in CONTACTS.items():
            if name.lower() in command:
                phone = number
                break

    if not phone:
        contacts_list = ", ".join(CONTACTS.keys()) if CONTACTS else "none saved"
        return (
            f"I need a phone number or contact name. "
            f"Your saved contacts: {contacts_list}. "
            f"Try: 'send message to +919876543210 saying Hello'"
        )

    # Extract message
    message = "Hello from FRIDAY!"
    for keyword in ["saying ", "message ", "that "]:
        if keyword in command:
            idx = command.index(keyword) + len(keyword)
            message = command[idx:].strip()
            break

    return send_whatsapp(phone, message)
