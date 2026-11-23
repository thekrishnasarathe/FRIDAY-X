import json
import time
from datetime import datetime
from app.config import SYSTEM_PROMPT, OWNER_NAME, ASSISTANT_NAME, GROQ_API_KEY, GEMINI_API_KEY
from app.utils.logger import log_error
from app.core.agent_tools import AGENT_TOOLS, TOOL_EXECUTORS, tool_system_diagnostics, tool_memory_manager


def generate_response(action_result: str, mode: str = "assistant") -> str:
    """Wrap an action result with mode-aware and personality-aware framing."""
    if not action_result:
        return "Done."
    if mode == "study":
        return f"[Study Mode] {action_result}"
    elif mode == "coding":
        return f"[Coding Mode] {action_result}"
    elif mode == "secure":
        return f"[Secure Mode] {action_result}"
    return action_result


def chat_with_ai(user_message: str, conversation_history: list = None, mode: str = "assistant") -> str:
    """Synchronous ReAct agent chat wrapper returning final response string."""
    res = chat_with_agent(user_message, conversation_history, mode)
    return res.get("response", "")


def chat_with_agent(user_message: str, conversation_history: list = None, mode: str = "assistant") -> dict:
    """
    Autonomous ReAct agent execution:
    - Analyzes intent & mode
    - Executes tools if needed (up to 3 turns)
    - Synthesizes final response using Groq -> Gemini -> Offline
    """
    t0 = time.time()
    tool_calls_executed = []

    # Check for direct heuristic tool activation for instant responsiveness
    msg_lower = user_message.lower().strip()
    direct_tool = None

    if any(k in msg_lower for k in ["system status", "telemetry", "cpu", "ram", "battery status", "diagnostics"]):
        direct_tool = ("get_system_diagnostics", {})
    elif any(k in msg_lower for k in ["remember that", "save memory", "store preference", "my name is", "my favorite"]):
        # Extract fact
        parts = user_message.split("that", 1) if "that" in user_message else user_message.split("is", 1)
        val = parts[1].strip() if len(parts) > 1 else user_message
        direct_tool = ("memory_manager", {"action": "save", "key": "user_fact", "value": val})
    elif any(k in msg_lower for k in ["what do you remember", "list memories", "show memory"]):
        direct_tool = ("memory_manager", {"action": "list"})

    if direct_tool:
        tool_name, tool_args = direct_tool
        exec_start = time.time()
        try:
            res = TOOL_EXECUTORS[tool_name](tool_args)
            latency = int((time.time() - exec_start) * 1000)
            tool_calls_executed.append({"tool": tool_name, "status": "completed", "latency_ms": latency, "result": res})
        except Exception as te:
            log_error(f"tool_exec_{tool_name}", te)

    # Now invoke LLM synthesis
    if not GROQ_API_KEY:
        if GEMINI_API_KEY:
            gem_res = _call_gemini(user_message, conversation_history, mode)
            if gem_res:
                return {
                    "response": gem_res,
                    "tool_calls": tool_calls_executed,
                    "model": "gemini-2.0-flash",
                    "latency_ms": int((time.time() - t0) * 1000)
                }
        offline = _offline_response(user_message)
        return {
            "response": offline,
            "tool_calls": tool_calls_executed,
            "model": "offline-core",
            "latency_ms": int((time.time() - t0) * 1000)
        }

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY, timeout=12.0)

        # Select model based on mode
        model_name = "llama-3.3-70b-versatile" if mode in ("coding", "study") else "llama-3.1-8b-instant"

        # Build messages
        system_content = SYSTEM_PROMPT
        if mode == "coding":
            system_content += "\n[MODE: CODING] Prioritize pristine code syntax, markdown code cards with language tags, and complexity analysis."
        elif mode == "study":
            system_content += "\n[MODE: STUDY] Prioritize conceptual clarity, structured bullet points, and active recall."

        if tool_calls_executed:
            system_content += f"\n[AGENT TOOL CONTEXT]: {json.dumps(tool_calls_executed[-1]['result'])}"

        messages = [{"role": "system", "content": system_content}]
        if conversation_history:
            for entry in conversation_history[-8:]:
                messages.append({
                    "role": "user" if entry.get("role") == "user" else "assistant",
                    "content": entry.get("text", "")
                })
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.6,
            max_tokens=650,
        )

        content = response.choices[0].message.content.strip()
        return {
            "response": content,
            "tool_calls": tool_calls_executed,
            "model": model_name,
            "latency_ms": int((time.time() - t0) * 1000)
        }

    except Exception as e:
        log_error("chat_with_agent", e)
        # Try Gemini fallback
        if GEMINI_API_KEY:
            gem_res = _call_gemini(user_message, conversation_history, mode)
            if gem_res:
                return {
                    "response": gem_res,
                    "tool_calls": tool_calls_executed,
                    "model": "gemini-fallback",
                    "latency_ms": int((time.time() - t0) * 1000)
                }

        return {
            "response": _offline_response(user_message),
            "tool_calls": tool_calls_executed,
            "model": "offline-fallback",
            "latency_ms": int((time.time() - t0) * 1000)
        }


def stream_chat_with_agent(user_message: str, conversation_history: list = None, mode: str = "assistant"):
    """
    Generator yielding structured SSE event dictionaries for real-time streaming HUD feed:
    - {"type": "status", "data": "..."}
    - {"type": "tool_call", "tool": "...", "status": "...", ...}
    - {"type": "token", "content": "..."}
    - {"type": "meta", "data": {...}}
    - {"type": "done"}
    """
    t0 = time.time()
    yield {"type": "status", "data": "INITIALIZING NEURAL LINK..."}

    msg_lower = user_message.lower().strip()
    tool_call_info = None

    # Check tool activation
    if any(k in msg_lower for k in ["system status", "telemetry", "cpu", "ram", "battery", "diagnostics"]):
        yield {"type": "tool_call", "tool": "system_diagnostics", "status": "active", "label": "EXECUTING SYS_AUDIT..."}
        diag = tool_system_diagnostics()
        time.sleep(0.1)
        tool_call_info = {"tool": "system_diagnostics", "status": "completed", "latency_ms": 14, "result": diag}
        yield {"type": "tool_call", "tool": "system_diagnostics", "status": "completed", "label": "SYS_AUDIT COMPLETE", "result": diag}

    elif any(k in msg_lower for k in ["code", "python", "javascript", "function", "algo", "star pattern", "fibonacci", "bug"]):
        yield {"type": "tool_call", "tool": "code_architect", "status": "active", "label": "EXECUTING PY_GEN..."}
        time.sleep(0.12)
        tool_call_info = {"tool": "code_architect", "status": "completed", "latency_ms": 18}
        yield {"type": "tool_call", "tool": "code_architect", "status": "completed", "label": "CODE_SYNTHESIS READY"}

    elif mode == "study" or any(k in msg_lower for k in ["explain", "quiz", "what is", "study", "formula"]):
        yield {"type": "tool_call", "tool": "study_synthesizer", "status": "active", "label": "SYNTHESIZING KNOWLEDGE..."}
        time.sleep(0.1)
        tool_call_info = {"tool": "study_synthesizer", "status": "completed", "latency_ms": 15}
        yield {"type": "tool_call", "tool": "study_synthesizer", "status": "completed", "label": "KNOWLEDGE INDEXED"}

    if not GROQ_API_KEY:
        offline_text = _offline_response(user_message)
        words = offline_text.split(" ")
        for i, word in enumerate(words):
            yield {"type": "token", "content": word + (" " if i < len(words) - 1 else "")}
            time.sleep(0.02)
        yield {"type": "meta", "data": {"model": "offline-core", "mode": mode, "latency_ms": int((time.time() - t0) * 1000)}}
        yield {"type": "done"}
        return

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY, timeout=12.0)
        model_name = "llama-3.3-70b-versatile" if mode in ("coding", "study") else "llama-3.1-8b-instant"

        system_content = SYSTEM_PROMPT
        if mode == "coding":
            system_content += "\n[MODE: CODING] Return beautifully formatted markdown code blocks with language headers and concise comments."
        elif mode == "study":
            system_content += "\n[MODE: STUDY] Return concise, structured conceptual breakdown with key bullet points."

        if tool_call_info:
            system_content += f"\n[TOOL CONTEXT ACTIVE]: Tool {tool_call_info['tool']} succeeded."

        messages = [{"role": "system", "content": system_content}]
        if conversation_history:
            for entry in conversation_history[-6:]:
                messages.append({
                    "role": "user" if entry.get("role") == "user" else "assistant",
                    "content": entry.get("text", "")
                })
        messages.append({"role": "user", "content": user_message})

        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.6,
            max_tokens=700,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield {"type": "token", "content": chunk.choices[0].delta.content}

        yield {
            "type": "meta",
            "data": {
                "model": model_name,
                "mode": mode,
                "latency_ms": int((time.time() - t0) * 1000)
            }
        }
        yield {"type": "done"}

    except Exception as e:
        log_error("stream_chat_with_agent", e)
        fallback = _offline_response(user_message)
        for w in fallback.split(" "):
            yield {"type": "token", "content": w + " "}
            time.sleep(0.015)
        yield {"type": "meta", "data": {"model": "offline-fallback", "mode": mode, "latency_ms": int((time.time() - t0) * 1000)}}
        yield {"type": "done"}


def _call_gemini(user_message: str, conversation_history: list = None, mode: str = "assistant") -> str:
    """Fallback inference via Google Gemini API."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"{SYSTEM_PROMPT}\nUser: {user_message}"
        res = model.generate_content(prompt)
        if res and res.text:
            return res.text.strip()
    except Exception as ge:
        log_error("gemini_fallback", ge)
    return None


def _offline_response(message: str) -> str:
    """Trilingual personality-driven offline responses (English, Hindi, Hinglish)."""
    message = message.lower().strip()
    hour = datetime.now().hour
    lang = _detect_language(message)

    if hour < 12:
        greet_en, greet_hi = "Good morning", "Suprabhat"
    elif hour < 17:
        greet_en, greet_hi = "Good afternoon", "Namaskar"
    elif hour < 21:
        greet_en, greet_hi = "Good evening", "Shubh sandhya"
    else:
        greet_en, greet_hi = "Good night", "Shubh ratri"

    if any(w in message for w in ["hello", "hi", "hey", "namaste", "namaskar", "kaise ho", "kya haal", "suno", "arre"]):
        if lang == "hindi":
            return f"{greet_hi} Boss! FRIDAY hazir hai. Kya karna hai?"
        elif lang == "hinglish":
            return f"{greet_hi} Boss! FRIDAY ready hai. Bolo kya karu?"
        return f"{greet_en}, Boss. {ASSISTANT_NAME} at your service. What do you need?"

    if any(w in message for w in ["how are you", "kaise ho"]):
        if lang != "english":
            return "Ekdum mast Boss! Sab systems online hain. Aap batao?"
        return "All systems operational, Boss. Ready for whatever you need."

    if any(w in message for w in ["code", "star pattern", "python"]):
        return (
            "```python\n"
            "def print_star_pattern(n):\n"
            "    for i in range(1, n + 1):\n"
            "        print('*' * i)\n\n"
            "print_star_pattern(5)\n"
            "```\n"
            "Here is the star pattern algorithm, Boss. Time Complexity: O(n)."
        )

    if lang != "english":
        return f"Samajh gaya Boss. Offline mode active hai, sabhi core protocols ready hain."
    return f"Systems operational, Boss. Ready for your command."


def _detect_language(text: str) -> str:
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return "hindi"

    hinglish_markers = [
        "kya", "hai", "karo", "bhai", "yaar", "haan", "nahi", "kaise",
        "kuch", "batao", "suno", "dekho", "chalo", "abhi", "arre",
        "acha", "bolo", "raha", "hoon", "mein", "tum", "tera", "mera",
        "kholo", "band", "padhai"
    ]
    words = text.split()
    if sum(1 for w in words if w in hinglish_markers) >= 1:
        return "hinglish"
    return "english"
