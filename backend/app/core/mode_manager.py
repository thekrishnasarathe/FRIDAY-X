CURRENT_MODE = "assistant"

def set_mode(mode_name: str) -> str:
    global CURRENT_MODE

    valid_modes = ["assistant", "study", "coding", "secure"]

    mode_name = mode_name.lower().strip()

    if mode_name not in valid_modes:
        return f"{mode_name} is not a valid mode."

    CURRENT_MODE = mode_name
    return f"{mode_name.capitalize()} mode activated."

def get_mode() -> str:
    return CURRENT_MODE