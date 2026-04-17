def classify_intent(command: str) -> str:
    """
    Classify the user's command into an intent category.
    Supports English, Hindi, and Hinglish keywords.
    Uses keyword matching with broad coverage + conversation fallback.
    """
    if not command:
        return "unknown"

    command = command.lower().strip()

    # ─── Greeting (EN + HI + Hinglish) ───────────────────
    greetings = [
        "hello", "hi ", "hey ", "good morning", "good afternoon",
        "good evening", "good night", "howdy", "what's up", "whats up",
        "namaste", "namaskar", "hola", "sup", "kaise ho", "kya haal",
        "suno", "arre", "bhai", "boss", "haan bhai", "kya chal raha",
    ]
    if any(command.startswith(g) or command == g.strip() for g in greetings):
        return "greeting"

    # ─── Mode switching ───────────────────────────────────
    if any(phrase in command for phrase in [
        "study mode", "coding mode", "assistant mode", "secure mode",
        "switch to", "activate mode", "change mode",
        "padhai mode", "code mode chalu", "mode badlo"
    ]):
        return "mode"

    # ─── Email ────────────────────────────────────────────
    if any(word in command for word in [
        "send email", "send mail", "compose email", "email to",
        "write email", "mail to", "email bhejo", "mail karo"
    ]):
        return "email"

    # ─── WhatsApp / messaging ─────────────────────────────
    if any(word in command for word in [
        "send message", "send whatsapp", "whatsapp message",
        "text message", "message to", "send msg",
        "message bhejo", "whatsapp karo", "msg bhej"
    ]):
        return "message"

    # ─── Time & date ──────────────────────────────────────
    if any(word in command for word in [
        "time", "date", "day", "clock", "what day",
        "samay", "kitne baje", "tarikh", "din kya hai", "time kya hai",
        "kya time hua", "kya baj rahe"
    ]):
        return "time_date"

    # ─── Weather ──────────────────────────────────────────
    if any(word in command for word in [
        "weather", "temperature", "forecast", "rain", "humid",
        "mausam", "barish", "garmi", "thand", "weather kaisa"
    ]):
        return "weather"

    # ─── News ─────────────────────────────────────────────
    if any(word in command for word in [
        "news", "headlines", "whats happening", "latest news",
        "khabar", "samachar", "kya chal raha duniya mein"
    ]):
        return "news"

    # ─── Jokes / fun ──────────────────────────────────────
    if any(word in command for word in [
        "joke", "funny", "make me laugh", "tell me something fun",
        "chutkula", "mazak", "hasao", "kuch funny suna",
        "joke suna", "hasa de"
    ]):
        return "joke"

    # ─── System info ──────────────────────────────────────
    import re
    system_keywords = [
        r"\bbattery\b", r"\bwifi\b", r"\bvolume\b", r"\bbrightness\b", r"\bcpu\b",
        r"\bram\b", r"\bmemory usage\b", r"\bdisk\b", r"\bsystem info\b",
        r"\bsystem status\b", r"\bshutdown\b", r"\brestart\b",
        r"\bsleep\b", r"\block\b", r"\block screen\b",
        r"\bbattery kitni\b", r"\bcharge\b", r"\bstatus batao\b",
        r"\bsystem kaisa\b"
    ]
    if any(re.search(pattern, command) for pattern in system_keywords):
        return "system"

    # ─── Search ───────────────────────────────────────────
    if any(word in command for word in [
        "search", "look up", "find on",
        "dhundho", "khojo", "search karo"
    ]):
        return "search"

    # ─── Screenshot/Vision ────────────────────────────────
    if any(word in command for word in [
        "screenshot", "screen capture", "photo le", "screen pakdo",
        "take screenshot", "ss le", "screen shot"
    ]):
        return "screenshot"

    # ─── Browser / website commands ───────────────────────
    website_keywords = [
        "youtube", "google", "github", "chatgpt", "instagram",
        "facebook", "linkedin", "wikipedia", "netflix", "spotify",
        "twitter", "reddit", "stackoverflow", "stack overflow",
        "website", "browser", "open website"
    ]
    if any(word in command for word in website_keywords):
        return "browser"

    # ─── App commands ─────────────────────────────────────
    app_keywords = [
        "whatsapp", "gemini", "file manager", "explorer",
        "microsoft store", "excel", "settings", "photos",
        "snipping tool", "calculator", "notepad", "word",
        "powerpoint", "vscode", "vs code", "chrome", "edge",
        "spotify", "terminal", "cmd", "powershell",
        "task manager", "clock", "paint", "camera",
        "calendar", "maps", "teams", "outlook"
    ]
    if any(word in command for word in app_keywords):
        return "application"

    # ─── Open generic ─────────────────────────────────────
    if command.startswith("open ") or command.startswith("kholo ") or command.startswith("chalu karo "):
        return "application"

    # ─── File commands ────────────────────────────────────
    if any(word in command for word in [
        "create folder", "create file", "delete file", "delete folder",
        "make folder", "make file", "new folder", "new file",
        "folder banao", "file banao"
    ]):
        return "file"

    # ─── Identity / about ────────────────────────────────
    if any(word in command for word in [
        "who are you", "your name", "what are you", "about you",
        "who made you", "who created you",
        "tu kaun hai", "tera naam kya", "kisne banaya",
        "tujhe kisne banaya"
    ]):
        return "identity"

    # ─── Fallback → conversational AI ─────────────────────
    return "conversation"