from app.modules.automation.app_control import open_application
from app.modules.automation.browser_control import open_website, search_website
from app.modules.automation.file_control import create_folder, create_file
from app.modules.automation.system_control import get_system_info, control_system
from app.modules.communication.email_sender import send_email_command
from app.modules.communication.whatsapp_sender import send_whatsapp_command
from app.modules.utilities.datetime_helper import get_datetime_info
from app.modules.utilities.weather_helper import get_weather
from app.modules.utilities.news_helper import get_news
from app.modules.utilities.joke_helper import get_joke
from app.modules.vision.screenshot_reader import take_screenshot
from app.utils.helpers import normalize_command, extract_after


def route_command(command: str, intent: str = None):
    """
    Route a command to the appropriate module based on intent.
    Returns a result string describing what was done.
    """
    original = command
    command = command.lower().strip()
    normalized = normalize_command(command)

    if not intent:
        from app.core.intent_classifier import classify_intent
        intent = classify_intent(command)

    # ─── TIME / DATE ──────────────────────────────────────
    if intent == "time_date":
        return get_datetime_info(command)

    # ─── WEATHER ──────────────────────────────────────────
    if intent == "weather":
        city = extract_after(command, "weather in") or extract_after(command, "weather")
        return get_weather(city.strip() if city else "")

    # ─── NEWS ─────────────────────────────────────────────
    if intent == "news":
        return get_news()

    # ─── JOKES ────────────────────────────────────────────
    if intent == "joke":
        return get_joke()

    # ─── SCREENSHOT ───────────────────────────────────────
    if intent == "screenshot":
        return take_screenshot()

    # ─── SYSTEM ───────────────────────────────────────────
    if intent == "system":
        if any(w in command for w in ["shutdown", "restart", "lock", "sleep"]):
            return control_system(command)
        return get_system_info(command)

    # ─── EMAIL ────────────────────────────────────────────
    if intent == "email":
        return send_email_command(command)

    # ─── WHATSAPP MESSAGE ─────────────────────────────────
    if intent == "message":
        return send_whatsapp_command(command)

    # ─── SEARCH ───────────────────────────────────────────
    if intent == "search" or normalized.startswith("search"):
        # Handle "search youtube for X", "search google X", "search X"
        text = normalized

        if "youtube" in text:
            query = extract_after(text, "youtube")
            if query:
                search_website(query, "youtube")
                return f"Searching YouTube for {query}"

        if "google" in text:
            query = extract_after(text, "google")
            if query:
                search_website(query, "google")
                return f"Searching Google for {query}"

        # Generic search
        query = text.replace("search", "").strip()
        if query:
            search_website(query)
            return f"Searching for {query}"

    # ─── OPEN WEBSITES ────────────────────────────────────
    if intent == "browser" or "open" in normalized:
        # Try to find a website keyword
        website_names = [
            "youtube", "google", "github", "chatgpt", "instagram",
            "facebook", "linkedin", "wikipedia", "netflix", "spotify",
            "twitter", "reddit", "stackoverflow", "stack overflow"
        ]
        for site in website_names:
            if site in command:
                # Check if also has "search" — hybrid command
                if "search" in command:
                    query = extract_after(command, "search")
                    if not query:
                        query = extract_after(command, site)
                    if query:
                        search_website(query, site)
                        return f"Searching {site.title()} for {query}"
                open_website(site)
                return f"Opening {site.title()}"

    # ─── OPEN APPLICATIONS ────────────────────────────────
    if intent == "application" or any(w in normalized for w in ["open", "kholo", "chalu karo"]):
        # Strip Hinglish prefixes to find the app name
        clean = command
        for prefix in ["open ", "kholo ", "chalu karo "]:
            if clean.startswith(prefix):
                clean = clean[len(prefix):].strip()
                break

        app_keywords = [
            "whatsapp", "gemini", "file manager", "explorer",
            "microsoft store", "excel", "settings", "photos",
            "snipping tool", "calculator", "notepad", "word",
            "powerpoint", "vscode", "vs code", "chrome", "edge",
            "spotify", "terminal", "cmd", "powershell",
            "task manager", "clock", "paint", "camera",
            "calendar", "maps", "teams", "outlook"
        ]
        for app in sorted(app_keywords, key=len, reverse=True):
            if app in command or app in clean:
                result = open_application(app)
                return result

        # If nothing matched but intent is application, try the cleaned name directly
        if clean:
            result = open_application(clean)
            return result

    # ─── FILE / FOLDER CREATION ───────────────────────────
    if intent == "file":
        if any(w in command for w in ["create folder", "make folder", "new folder"]):
            for prefix in ["create folder", "make folder", "new folder"]:
                if prefix in command:
                    folder_name = extract_after(command, prefix)
                    # Strip trailing " on desktop" etc.
                    folder_name = folder_name.replace("on desktop", "").strip()
                    if folder_name:
                        return create_folder(folder_name)

        if any(w in command for w in ["create file", "make file", "new file"]):
            for prefix in ["create file", "make file", "new file"]:
                if prefix in command:
                    file_name = extract_after(command, prefix)
                    file_name = file_name.replace("on desktop", "").strip()
                    if file_name:
                        return create_file(file_name)

    # ─── IDENTITY ─────────────────────────────────────────
    if intent == "identity":
        from app.config import ASSISTANT_NAME, OWNER_NAME
        return (
            f"I'm {ASSISTANT_NAME}, your personal AI assistant. "
            f"I was created by {OWNER_NAME}. Think of me as your digital right hand — "
            f"always online, always ready."
        )

    return None  # Let the brain handle it via AI