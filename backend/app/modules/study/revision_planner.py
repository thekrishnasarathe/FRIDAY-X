from app.utils.logger import log_error


def create_revision_plan(subject: str, days: int = 7) -> str:
    """Generate a revision plan for a subject over N days."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key needed for revision planning."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"You are FRIDAY, a study planner. Create a {days}-day revision plan for: {subject}\n"
            f"Format:\n"
            f"Day 1: [topics to cover]\n"
            f"Day 2: [topics to cover]\n"
            f"...\n"
            f"Keep each day's plan to 1-2 sentences. Be practical."
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't generate a revision plan right now."

    except Exception as e:
        log_error("create_revision_plan", e)
        return f"Revision planning failed: {str(e)}"


def suggest_resources(topic: str) -> str:
    """Suggest learning resources for a topic."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key needed for resource suggestions."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"Suggest 5 free learning resources for: {topic}\n"
            f"Include YouTube channels, websites, or courses. "
            f"Format as a numbered list with brief descriptions."
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't find resources right now."

    except Exception as e:
        log_error("suggest_resources", e)
        return f"Resource suggestion failed: {str(e)}"
