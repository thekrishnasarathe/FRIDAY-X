import os
import subprocess
from app.utils.logger import log_error


def open_application(app_name: str) -> str:
    """Open a Windows application by name with fuzzy matching."""
    app_name = app_name.lower().strip()

    apps = {
        # --- System apps ---
        "calculator": "start calc",
        "notepad": "start notepad",
        "paint": "start mspaint",
        "settings": "start ms-settings:",
        "file manager": "explorer",
        "explorer": "explorer",
        "photos": "start ms-photos:",
        "camera": "start microsoft.windows.camera:",
        "clock": "start ms-clock:",
        "calendar": "start outlookcal:",
        "maps": "start bingmaps:",
        "snipping tool": "start snippingtool",
        "task manager": "taskmgr",

        # --- Microsoft Office ---
        "excel": "start excel",
        "word": "start winword",
        "powerpoint": "start powerpnt",
        "outlook": "start outlook",
        "teams": "start msteams:",

        # --- Microsoft Store apps ---
        "whatsapp": "start whatsapp:",
        "microsoft store": "start ms-windows-store:",
        "spotify": "start spotify:",

        # --- Browsers ---
        "chrome": "start chrome",
        "edge": "start msedge",

        # --- Dev tools ---
        "vscode": "start code",
        "vs code": "start code",
        "terminal": "start wt",
        "cmd": "start cmd",
        "powershell": "start powershell",

        # --- Web-based (open in browser) ---
        "gemini": "start https://gemini.google.com",
    }

    command = apps.get(app_name)

    if not command:
        # Fuzzy match: try partial matching
        for key in apps:
            if app_name in key or key in app_name:
                command = apps[key]
                app_name = key
                break

    if not command:
        return f"Application '{app_name}' not found in my list."

    try:
        os.system(command)
        return f"Opening {app_name.title()}."
    except Exception as e:
        log_error("open_application", e)
        return f"Failed to open {app_name}: {str(e)}"