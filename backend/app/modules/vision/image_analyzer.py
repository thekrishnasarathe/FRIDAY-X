from app.utils.logger import log_error


def analyze_image(image_path: str) -> str:
    """
    Analyze an image using Gemini Vision.
    Requires google-generativeai with vision support.
    """
    try:
        import os
        if not os.path.exists(image_path):
            return f"Image not found: {image_path}"

        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Image analysis requires your Gemini API key."

        import google.generativeai as genai
        from PIL import Image

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        img = Image.open(image_path)

        response = model.generate_content([
            "You are FRIDAY, an AI assistant. Describe this image concisely in 2-3 sentences. "
            "Focus on the key content — what's shown, any text, any important details.",
            img
        ])

        if response and response.text:
            return response.text.strip()

        return "Couldn't analyze the image."

    except ImportError:
        return "Image analysis requires Pillow. Install: pip install Pillow"
    except Exception as e:
        log_error("analyze_image", e)
        return f"Image analysis failed: {str(e)}"


def describe_screenshot() -> str:
    """Take a screenshot and describe what's on screen."""
    try:
        import pyautogui
        import os
        from datetime import datetime

        temp_dir = os.path.join(os.path.expanduser("~"), "Desktop", "FRIDAY_Screenshots")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, "temp_analysis.png")

        pyautogui.screenshot().save(temp_path)
        return analyze_image(temp_path)

    except Exception as e:
        log_error("describe_screenshot", e)
        return f"Screenshot analysis failed: {str(e)}"
