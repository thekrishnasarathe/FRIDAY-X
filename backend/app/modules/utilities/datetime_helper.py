from datetime import datetime
import calendar


def get_datetime_info(command: str = "") -> str:
    """
    Return current time, date, or day info based on the command.
    """
    now = datetime.now()
    command = command.lower()

    if "time" in command:
        return f"It's {now.strftime('%I:%M %p')} right now."

    if "date" in command:
        return f"Today's date is {now.strftime('%B %d, %Y')}."

    if "day" in command:
        return f"Today is {now.strftime('%A')}."

    if "year" in command:
        return f"The year is {now.year}."

    if "month" in command:
        return f"We're in {now.strftime('%B')}."

    # Default: give both
    return (
        f"It's {now.strftime('%A, %B %d, %Y')} and the time is "
        f"{now.strftime('%I:%M %p')}."
    )
