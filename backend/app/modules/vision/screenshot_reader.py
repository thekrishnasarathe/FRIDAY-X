import os
import subprocess
from app.utils.logger import log_error


def take_screenshot(save_path: str = None) -> str:
    """Take a screenshot and save it."""
    try:
        import pyautogui
        from datetime import datetime

        if not save_path:
            screenshots_dir = os.path.join(os.path.expanduser("~"), "Desktop", "FRIDAY_Screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")

        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return f"Screenshot saved to {save_path}"

    except ImportError:
        return "Screenshot requires PyAutoGUI. It should already be installed."
    except Exception as e:
        log_error("take_screenshot", e)
        return f"Failed to take screenshot: {str(e)}"


def read_screenshot_text(image_path: str = None) -> str:
    """
    Take a screenshot and try to extract text from it.
    Requires pytesseract + Tesseract OCR installed.
    """
    try:
        # Take screenshot if no path given
        if not image_path:
            import pyautogui
            from datetime import datetime
            temp_dir = os.path.join(os.path.expanduser("~"), "Desktop", "FRIDAY_Screenshots")
            os.makedirs(temp_dir, exist_ok=True)
            image_path = os.path.join(temp_dir, "temp_screenshot.png")
            pyautogui.screenshot().save(image_path)

        # Try OCR
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            if text.strip():
                return f"Text from screenshot:\n{text.strip()[:500]}"
            return "No text found in the screenshot."
        except ImportError:
            return (
                "OCR requires pytesseract and Tesseract OCR.\n"
                "Install: pip install pytesseract\n"
                "Also install Tesseract: https://github.com/tesseract-ocr/tesseract"
            )

    except Exception as e:
        log_error("read_screenshot_text", e)
        return f"Screenshot reading failed: {str(e)}"
