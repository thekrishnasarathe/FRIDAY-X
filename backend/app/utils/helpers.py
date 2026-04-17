import re

# Words that don't add meaning to commands
FILLER_WORDS = [
    "please", "can you", "could you", "would you", "hey friday",
    "friday", "hey", "hi", "ok", "okay", "just", "kindly",
    "i want you to", "i need you to", "go ahead and", "can you please",
    "would you please", "will you", "yo", "bro", "dude",
]


def normalize_command(text: str) -> str:
    """Strip filler words and normalize a command for matching."""
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation

    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        text = text.replace(filler, "")

    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_after(text: str, keyword: str) -> str:
    """Extract everything after a keyword in a string."""
    text = text.lower()
    keyword = keyword.lower()
    idx = text.find(keyword)
    if idx == -1:
        return ""
    return text[idx + len(keyword):].strip()


def clean_text(text: str) -> str:
    """Basic text cleanup."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
