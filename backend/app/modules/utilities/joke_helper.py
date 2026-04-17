import random
import requests
from app.utils.logger import log_error


# Built-in jokes for offline fallback
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "There are only 10 types of people in the world: those who understand binary, and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "What's a computer's favorite snack? Microchips.",
    "Why did the developer go broke? Because he used up all his cache.",
    "What do you call a computer that sings? A-Dell.",
    "Why do Java developers wear glasses? Because they can't C#.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "My code doesn't have bugs. It has unexpected features.",
    "In order to understand recursion, one must first understand recursion.",
    "There's no place like 127.0.0.1.",
    "Algorithm: A word used by programmers when they don't want to explain what they did.",
]


def get_joke() -> str:
    """Get a random joke — tries online first, falls back to built-in."""
    try:
        response = requests.get(
            "https://v2.jokeapi.dev/joke/Programming,Miscellaneous?type=single",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("joke"):
                return data["joke"]

    except Exception as e:
        log_error("get_joke", e)

    return random.choice(JOKES)
