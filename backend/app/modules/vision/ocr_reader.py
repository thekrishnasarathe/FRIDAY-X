from app.utils.logger import log_error


def extract_text(image_path: str) -> str:
    """Extract text from an image using OCR."""
    try:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return (
                "OCR requires pytesseract and Pillow.\n"
                "Install: pip install pytesseract Pillow\n"
                "Also install Tesseract OCR engine."
            )

        import os
        if not os.path.exists(image_path):
            return f"Image not found: {image_path}"

        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        if text.strip():
            return f"Extracted text:\n{text.strip()[:1000]}"
        return "No text found in the image."

    except Exception as e:
        log_error("extract_text", e)
        return f"OCR failed: {str(e)}"


def extract_text_from_region(image_path: str, x: int, y: int, w: int, h: int) -> str:
    """Extract text from a specific region of an image."""
    try:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return "OCR requires pytesseract and Pillow."

        img = Image.open(image_path)
        region = img.crop((x, y, x + w, y + h))
        text = pytesseract.image_to_string(region)

        if text.strip():
            return f"Text from region:\n{text.strip()}"
        return "No text found in the selected region."

    except Exception as e:
        log_error("extract_text_from_region", e)
        return f"Regional OCR failed: {str(e)}"
