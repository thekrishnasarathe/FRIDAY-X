import requests
import time
from app.utils.logger import log_error

_weather_cache = {}
CACHE_TTL = 900  # 15 minutes

def get_weather(city: str = "") -> str:
    """
    Get weather info using wttr.in (no API key needed).
    Uses caching (15 min) to save network data.
    """
    if not city:
        city = ""  # wttr.in will auto-detect location

    now = time.time()
    if city in _weather_cache:
        cached_data, cached_time = _weather_cache[city]
        if now - cached_time < CACHE_TTL:
            return cached_data

    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            weather = response.text.strip()
            result = f"Current weather: {weather}"
            _weather_cache[city] = (result, now)
            return result

        return "Couldn't fetch weather data right now."

    except Exception as e:
        log_error("get_weather", e)
        return "Weather service is unavailable at the moment."
