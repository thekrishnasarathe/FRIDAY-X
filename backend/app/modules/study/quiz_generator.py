from app.utils.logger import log_error


def generate_quiz(topic: str, num_questions: int = 5) -> str:
    """Use Gemini to generate a quiz on a topic."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key needed for quiz generation."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"You are FRIDAY, a study assistant. Generate {num_questions} "
            f"multiple choice questions on: {topic}\n\n"
            f"Format each question as:\n"
            f"Q1. [question]\n"
            f"  a) [option]\n  b) [option]\n  c) [option]\n  d) [option]\n"
            f"Answer: [letter]\n\n"
            f"Make them educational and progressively harder."
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't generate a quiz right now."

    except Exception as e:
        log_error("generate_quiz", e)
        return f"Quiz generation failed: {str(e)}"


def generate_flashcards(topic: str, count: int = 5) -> str:
    """Generate flashcard-style Q&A pairs on a topic."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key needed for flashcards."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"Generate {count} flashcards for studying: {topic}\n"
            f"Format: Q: [question]\\nA: [concise answer]\\n\\n"
            f"Keep answers to 1-2 sentences."
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't generate flashcards right now."

    except Exception as e:
        log_error("generate_flashcards", e)
        return f"Flashcard generation failed: {str(e)}"
