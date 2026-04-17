import os
from app.utils.logger import log_error

DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")


def create_project(project_name: str, project_type: str = "python") -> str:
    """Create a starter project structure on the Desktop."""
    try:
        project_path = os.path.join(DESKTOP_PATH, project_name)
        os.makedirs(project_path, exist_ok=True)

        if project_type == "python":
            return _create_python_project(project_path, project_name)
        elif project_type == "web":
            return _create_web_project(project_path, project_name)
        else:
            return _create_basic_project(project_path, project_name)

    except Exception as e:
        log_error("create_project", e)
        return f"Failed to create project: {str(e)}"


def _create_python_project(path: str, name: str) -> str:
    """Create a Python project structure."""
    folders = ["src", "tests", "docs"]
    for folder in folders:
        os.makedirs(os.path.join(path, folder), exist_ok=True)

    files = {
        "main.py": f'"""\n{name} - Created by FRIDAY\n"""\n\ndef main():\n    print("Hello from {name}!")\n\nif __name__ == "__main__":\n    main()\n',
        "requirements.txt": "# Add your dependencies here\n",
        "README.md": f"# {name}\n\nCreated by FRIDAY-X Assistant.\n",
        ".gitignore": "__pycache__/\n*.pyc\nvenv/\n.env\n",
        os.path.join("src", "__init__.py"): "",
        os.path.join("tests", "__init__.py"): "",
    }

    for filepath, content in files.items():
        full_path = os.path.join(path, filepath)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return f"Python project '{name}' created on Desktop with src/, tests/, docs/, main.py, and requirements.txt."


def _create_web_project(path: str, name: str) -> str:
    """Create a basic web project structure."""
    folders = ["css", "js", "assets"]
    for folder in folders:
        os.makedirs(os.path.join(path, folder), exist_ok=True)

    files = {
        "index.html": f'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{name}</title>\n    <link rel="stylesheet" href="css/style.css">\n</head>\n<body>\n    <h1>{name}</h1>\n    <script src="js/main.js"></script>\n</body>\n</html>\n',
        os.path.join("css", "style.css"): "* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}\n\nbody {\n    font-family: sans-serif;\n}\n",
        os.path.join("js", "main.js"): f'console.log("{name} loaded!");\n',
        "README.md": f"# {name}\n\nCreated by FRIDAY-X Assistant.\n",
    }

    for filepath, content in files.items():
        full_path = os.path.join(path, filepath)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return f"Web project '{name}' created on Desktop with index.html, css/, js/, and assets/."


def _create_basic_project(path: str, name: str) -> str:
    """Create a minimal project structure."""
    files = {
        "README.md": f"# {name}\n\nCreated by FRIDAY-X Assistant.\n",
        "main.py": f'# {name}\nprint("Hello from {name}!")\n',
    }

    for filepath, content in files.items():
        full_path = os.path.join(path, filepath)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return f"Basic project '{name}' created on Desktop."
