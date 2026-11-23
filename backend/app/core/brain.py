from app.core.intent_classifier import classify_intent
from app.core.mode_manager import get_mode, set_mode
from app.core.response_engine import generate_response, chat_with_ai
from app.core.command_router import route_command
from app.modules.memory.session_memory import save_command
from app.utils.logger import log_command, log_error
from app.utils.helpers import normalize_command

# Conversation history for context (in-memory, per session)
_conversation_history = []
MAX_HISTORY = 20


def process_command(command: str) -> str:
    """
    Main FRIDAY brain pipeline:
    1. Normalize input
    2. Classify intent
    3. Handle mode switching
    4. Route actionable commands
    5. Fall back to AI conversation for everything else
    6. Log everything
    """
    if not command or not command.strip():
        return "I didn't catch that. Could you say it again?"

    original = command
    command = command.strip()
    intent = classify_intent(command)

    try:
        # ─── MODE SWITCHING ──────────────────────────────
        if intent == "mode":
            for mode in ["study", "coding", "assistant", "secure"]:
                if mode in command.lower():
                    response = set_mode(mode)
                    _log_and_save(original, response)
                    return response

        # ─── GREETING ────────────────────────────────────
        if intent == "greeting":
            response = chat_with_ai(command, _conversation_history, mode=get_mode())
            _log_and_save(original, response)
            return response

        # ─── ACTIONABLE COMMANDS ─────────────────────────
        if intent not in ("conversation", "greeting"):
            result = route_command(command, intent)
            if result:
                current_mode = get_mode()
                response = generate_response(result, current_mode)
                _log_and_save(original, response)
                return response

        # ─── CONVERSATIONAL AI FALLBACK ──────────────────
        response = chat_with_ai(command, _conversation_history, mode=get_mode())
        _log_and_save(original, response)
        return response

    except Exception as e:
        log_error("brain.process_command", e)
        return "Something went wrong on my end. Give me a moment and try again."


def _log_and_save(command: str, response: str):
    """Log and save to memory."""
    global _conversation_history

    log_command(command, response)
    save_command(command, response)

    # Keep conversation history for AI context
    _conversation_history.append({"role": "user", "text": command})
    _conversation_history.append({"role": "assistant", "text": response})

    # Trim history
    if len(_conversation_history) > MAX_HISTORY * 2:
        _conversation_history = _conversation_history[-(MAX_HISTORY * 2):]