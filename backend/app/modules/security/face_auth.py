from app.utils.logger import log_error


def verify_face() -> str:
    """
    Face authentication placeholder.
    Full implementation requires OpenCV and face_recognition.
    """
    try:
        try:
            import cv2
        except ImportError:
            return (
                "Face auth requires OpenCV. Install with: pip install opencv-python\n"
                "Also install face_recognition: pip install face_recognition"
            )

        return (
            "Face authentication module is ready. "
            "Face enrollment and verification can be set up with OpenCV + face_recognition."
        )

    except Exception as e:
        log_error("verify_face", e)
        return f"Face auth error: {str(e)}"


def is_face_auth_available() -> bool:
    """Check if face auth dependencies are installed."""
    try:
        import cv2
        return True
    except ImportError:
        return False
