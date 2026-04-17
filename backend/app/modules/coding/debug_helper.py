from app.utils.logger import log_error


def analyze_error(error_message: str, language: str = "python") -> str:
    """Use Gemini to analyze an error message and suggest fixes."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key needed for debug analysis."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"You are FRIDAY, a concise debugging assistant. "
            f"Analyze this {language} error and give a fix in 2-3 sentences:\n\n"
            f"Error: {error_message}"
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't analyze the error right now."

    except Exception as e:
        log_error("analyze_error", e)
        return f"Debug analysis failed: {str(e)}"


def check_syntax(code: str, language: str = "python") -> str:
    """Check Python code for syntax errors."""
    if language != "python":
        return f"Syntax checking for {language} is not supported yet."

    try:
        compile(code, "<string>", "exec")
        return "No syntax errors found. Code looks clean."
    except SyntaxError as e:
        return f"Syntax error on line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"Check failed: {str(e)}"
