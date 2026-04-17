import requests
from app.utils.logger import log_error


def get_weather(city: str = "") -> str:
    """
    Get weather info using wttr.in (no API key needed).
    """
    if not city:
        city = ""  # wttr.in will auto-detect location

    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            weather = response.text.strip()
            return f"Current weather: {weather}"

        return "Couldn't fetch weather data right now."

    except Exception as e:
        log_error("get_weather", e)
        return "Weather service is unavailable at the moment."
