from datetime import datetime
from app.config import SYSTEM_PROMPT, GEMINI_API_KEY, OWNER_NAME, ASSISTANT_NAME
from app.utils.logger import log_error


def generate_response(action_result: str, mode: str = "assistant") -> str:
    """
    Wrap an action result with mode-aware and personality-aware framing.
    """
    if not action_result:
        return "Done."

    # Add mode prefix only for non-assistant modes
    if mode == "study":
        return f"[Study Mode] {action_result}"
    elif mode == "coding":
        return f"[Coding Mode] {action_result}"
    elif mode == "secure":
        return f"[Secure Mode] {action_result}"

    return action_result


def chat_with_ai(user_message: str, conversation_history: list = None) -> str:
    """
    Send a message to Google Gemini for natural, Jarvis-style conversation.
    Supports English, Hindi, and Hinglish automatically.
    Falls back to a personality-driven offline response if no API key.
    Includes retry logic for rate limits.
    """
    if not GEMINI_API_KEY:
        return _offline_response(user_message)

    import time

    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Build conversation context
        messages = [SYSTEM_PROMPT + "\n\n"]

        if conversation_history:
            for entry in conversation_history[-10:]:
                role = entry.get("role", "user")
                text = entry.get("text", "")
                if role == "user":
                    messages.append(f"User: {text}")
                else:
                    messages.append(f"FRIDAY: {text}")

        messages.append(f"User: {user_message}")
        messages.append("FRIDAY:")

        prompt = "\n".join(messages)

        # Retry with backoff for rate limits
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)

                if response and response.text:
                    return response.text.strip()

                return _offline_response(user_message)

            except Exception as retry_error:
                error_str = str(retry_error).lower()
                if "429" in error_str or "quota" in error_str or "rate" in error_str:
                    wait_time = (attempt + 1) * 2  # 2s, 4s, 6s
                    log_error("chat_with_ai", Exception(f"Rate limited, retrying in {wait_time}s..."))
                    time.sleep(wait_time)
                    continue
                else:
                    raise retry_error

        return _offline_response(user_message)

    except Exception as e:
        log_error("chat_with_ai", e)
        return _offline_response(user_message)


def _offline_response(message: str) -> str:
    """
    Provide trilingual personality-driven responses when Gemini is unavailable.
    Auto-detects Hindi/Hinglish/English and responds accordingly.
    """
    message = message.lower().strip()
    hour = datetime.now().hour
    lang = _detect_language(message)

    # Time-based greeting
    if hour < 12:
        greet_en, greet_hi = "Good morning", "Suprabhat"
    elif hour < 17:
        greet_en, greet_hi = "Good afternoon", "Namaskar"
    elif hour < 21:
        greet_en, greet_hi = "Good evening", "Shubh sandhya"
    else:
        greet_en, greet_hi = "Good night", "Shubh ratri"

    # ─── GREETINGS ────────────────────────────────────────
    if any(w in message for w in ["hello", "hi", "hey", "namaste", "namaskar",
                                   "kaise ho", "kya haal", "suno", "arre"]):
        if lang == "hindi":
            return f"{greet_hi} Boss! FRIDAY hazir hai. Kya karna hai?"
        elif lang == "hinglish":
            return f"{greet_hi} Boss! FRIDAY ready hai. Bolo kya karu?"
        return f"{greet_en}, Boss. {ASSISTANT_NAME} at your service. What do you need?"

    # ─── HOW ARE YOU ──────────────────────────────────────
    if any(w in message for w in ["how are you", "how do you feel", "kaise ho", "kaisa hai"]):
        if lang != "english":
            return f"Ekdum mast Boss! Sab systems chalu hain. Aap batao?"
        return f"All systems operational, Boss. Ready for whatever you need."

    # ─── THANKS ───────────────────────────────────────────
    if any(w in message for w in ["thank", "thanks", "shukriya", "dhanyavaad", "thx"]):
        if lang != "english":
            return "Are Boss, yeh toh mera kaam hai! Aur kuch?"
        return f"Anytime, Boss."

    # ─── IDENTITY ─────────────────────────────────────────
    if any(w in message for w in ["who are you", "your name", "what are you",
                                   "tu kaun", "tera naam", "kisne banaya"]):
        if lang != "english":
            return (
                f"Main {ASSISTANT_NAME} hoon Boss, aapka personal AI assistant. "
                f"{OWNER_NAME} ne banaya hai mujhe. Humesha ready!"
            )
        return (
            f"I'm {ASSISTANT_NAME}, your personal AI assistant. "
            f"Built by {OWNER_NAME}, inspired by the legends."
        )

    # ─── GOODBYE ──────────────────────────────────────────
    if any(w in message for w in ["bye", "goodbye", "see you", "good night",
                                   "alvida", "chalo", "band karo"]):
        if lang != "english":
            return f"Alvida Boss! Systems standby pe hain. Jab zaroorat ho, bula lena."
        return f"Until next time, Boss. Systems on standby."

    # ─── FALLBACK ─────────────────────────────────────────
    if lang != "english":
        return (
            f"Samajh gaya Boss. Lekin agar Gemini API key lagao toh "
            f"main full power pe kaam karunga. Abhi offline mode mein hoon."
        )
    return (
        f"I hear you, Boss. I'd give a smarter answer with "
        f"my AI brain connected. Add your Gemini API key to unlock full mode."
    )


def _detect_language(text: str) -> str:
    """
    Simple language detection for English vs Hindi vs Hinglish.
    """
    # Check for Devanagari script → pure Hindi
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return "hindi"

    # Common Hinglish words
    hinglish_markers = [
        "kya", "hai", "karo", "bhai", "yaar", "haan", "nahi", "kaise",
        "kuch", "batao", "suno", "dekho", "chalo", "abhi", "arre",
        "acha", "bolo", "raha", "hoon", "mein", "tum", "tera", "mera",
        "kahan", "kaun", "kitna", "bohot", "bahut", "thoda", "zyada",
        "samajh", "sab", "kholo", "band", "bhejo", "dikha", "bata",
        "chal", "kar", "le", "de", "ho", "ji", "na", "toh",
        "padhai", "padhao", "banao", "dhundho", "khojo"
    ]

    words = text.split()
    hinglish_count = sum(1 for w in words if w in hinglish_markers)

    if hinglish_count >= 1 and len(words) <= 5:
        return "hinglish"
    if hinglish_count >= 2:
        return "hinglish"

    return "english"