from app.utils.logger import log_error


def execute_workflow(workflow_name: str, steps: list = None) -> str:
    """
    Execute a multi-step workflow (sequence of commands).
    """
    if not steps:
        steps = _get_preset_workflow(workflow_name)

    if not steps:
        return f"Workflow '{workflow_name}' not found. Available: {', '.join(PRESET_WORKFLOWS.keys())}"

    results = []
    from app.core.brain import process_command

    for i, step in enumerate(steps, 1):
        try:
            result = process_command(step)
            results.append(f"  Step {i}: {step} → {result}")
        except Exception as e:
            results.append(f"  Step {i}: {step} → FAILED: {str(e)}")
            break

    return f"Workflow '{workflow_name}' completed:\n" + "\n".join(results)


# ─── Preset Workflows ─────────────────────────────────────
PRESET_WORKFLOWS = {
    "morning": [
        "what time is it",
        "whats the weather",
        "open gmail",
        "open whatsapp",
    ],
    "coding": [
        "switch to coding mode",
        "open vscode",
        "open github",
        "open chatgpt",
    ],
    "study": [
        "switch to study mode",
        "open youtube",
        "open google",
    ],
    "research": [
        "open google",
        "open wikipedia",
        "open chatgpt",
    ],
    "social": [
        "open whatsapp",
        "open instagram",
        "open twitter",
    ],
}


def _get_preset_workflow(name: str) -> list:
    """Get a preset workflow by name."""
    return PRESET_WORKFLOWS.get(name.lower().strip(), [])


def list_workflows() -> str:
    """List all available preset workflows."""
    lines = []
    for name, steps in PRESET_WORKFLOWS.items():
        lines.append(f"  {name}: {' → '.join(steps)}")
    return "Available workflows:\n" + "\n".join(lines)