import os
import subprocess
from app.utils.logger import log_error


def explain_code(language: str, code_snippet: str) -> str:
    """Use Gemini to explain a code snippet."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "I need the Gemini API key to explain code. Add it to your .env file."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"You are FRIDAY, a coding assistant. Explain this {language} code "
            f"concisely in 2-4 sentences. Be clear and practical.\n\n"
            f"```{language}\n{code_snippet}\n```"
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't analyze that code right now."

    except Exception as e:
        log_error("explain_code", e)
        return f"Code analysis failed: {str(e)}"


def run_python_code(code: str) -> str:
    """Run a Python code snippet safely and return output."""
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        error = result.stderr.strip()

        if error:
            return f"Error:\n{error}"
        if output:
            return f"Output:\n{output}"
        return "Code executed successfully. No output."

    except subprocess.TimeoutExpired:
        return "Code execution timed out (10s limit)."
    except Exception as e:
        log_error("run_python_code", e)
        return f"Execution failed: {str(e)}"


def get_code_suggestion(prompt: str) -> str:
    """Get an AI-powered code suggestion."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key required for code suggestions."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        full_prompt = (
            f"You are FRIDAY, a coding assistant. Write concise, clean code for: {prompt}\n"
            f"Return ONLY the code with brief comments. No explanations outside the code."
        )
        response = model.generate_content(full_prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't generate code right now."

    except Exception as e:
        log_error("get_code_suggestion", e)
        return f"Code suggestion failed: {str(e)}"
