import os

DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

def create_folder(folder_name: str) -> str:
    try:
        folder_path = os.path.join(DESKTOP_PATH, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return f"Folder '{folder_name}' created successfully on Desktop."
    except Exception as e:
        return f"Failed to create folder: {str(e)}"

def create_file(file_name: str) -> str:
    try:
        file_path = os.path.join(DESKTOP_PATH, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        return f"File '{file_name}' created successfully on Desktop."
    except Exception as e:
        return f"Failed to create file: {str(e)}"