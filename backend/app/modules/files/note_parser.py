import os
from app.utils.logger import log_error


def read_file(filepath: str) -> str:
    """Read and return contents of a text file."""
    try:
        if not os.path.exists(filepath):
            return f"File not found: {filepath}"

        if not os.path.isfile(filepath):
            return f"'{filepath}' is not a file."

        size = os.path.getsize(filepath)
        if size > 50000:  # 50KB limit
            return f"File is too large ({size} bytes). Max 50KB."

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if not content.strip():
            return "File is empty."

        return content

    except Exception as e:
        log_error("read_file", e)
        return f"Failed to read file: {str(e)}"


def write_to_file(filepath: str, content: str, append: bool = False) -> str:
    """Write content to a text file."""
    try:
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        mode = "a" if append else "w"

        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)

        action = "Appended to" if append else "Written to"
        return f"{action} {os.path.basename(filepath)}."

    except Exception as e:
        log_error("write_to_file", e)
        return f"Failed to write file: {str(e)}"


def get_file_info(filepath: str) -> str:
    """Get info about a file."""
    try:
        if not os.path.exists(filepath):
            return f"File not found: {filepath}"

        stat = os.stat(filepath)
        size_kb = round(stat.st_size / 1024, 1)
        _, ext = os.path.splitext(filepath)

        from datetime import datetime
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%b %d, %Y %I:%M %p")

        return (
            f"File: {os.path.basename(filepath)}\n"
            f"  Type: {ext or 'no extension'}\n"
            f"  Size: {size_kb} KB\n"
            f"  Modified: {modified}\n"
            f"  Path: {filepath}"
        )

    except Exception as e:
        log_error("get_file_info", e)
        return f"Failed to get file info: {str(e)}"
