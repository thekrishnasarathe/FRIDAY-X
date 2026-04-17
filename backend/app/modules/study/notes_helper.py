import os
import json
from datetime import datetime
from app.utils.logger import log_error

NOTES_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "FRIDAY_Notes")


def create_note(title: str, content: str = "") -> str:
    """Create a text note on the Desktop in FRIDAY_Notes folder."""
    try:
        os.makedirs(NOTES_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
        filename = f"{safe_title}_{timestamp}.txt"
        filepath = os.path.join(NOTES_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n")
            f.write(f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            if content:
                f.write(content)

        return f"Note '{title}' created in FRIDAY_Notes folder."

    except Exception as e:
        log_error("create_note", e)
        return f"Failed to create note: {str(e)}"


def list_notes() -> str:
    """List all notes in the FRIDAY_Notes folder."""
    try:
        if not os.path.exists(NOTES_DIR):
            return "No notes found. Create your first note!"

        notes = [f for f in os.listdir(NOTES_DIR) if f.endswith(('.txt', '.md'))]
        if not notes:
            return "No notes found."

        note_list = "\n".join(f"  {i+1}. {n}" for i, n in enumerate(notes[:20]))
        return f"Your notes ({len(notes)} total):\n{note_list}"

    except Exception as e:
        log_error("list_notes", e)
        return f"Failed to list notes: {str(e)}"


def summarize_topic(topic: str) -> str:
    """Use Gemini to generate a study summary on a topic."""
    try:
        from app.config import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return "Gemini API key needed for study summaries."

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = (
            f"You are FRIDAY, a study assistant. Give a concise, clear summary of: {topic}\n"
            f"Use bullet points. Keep it under 150 words. Make it student-friendly."
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

        return "Couldn't generate a summary right now."

    except Exception as e:
        log_error("summarize_topic", e)
        return f"Summary generation failed: {str(e)}"
