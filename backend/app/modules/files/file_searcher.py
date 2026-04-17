import os
from app.utils.logger import log_error

SEARCH_ROOTS = [
    os.path.join(os.path.expanduser("~"), "Desktop"),
    os.path.join(os.path.expanduser("~"), "Documents"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
]


def search_files(query: str, file_type: str = None, max_results: int = 10) -> str:
    """Search for files by name across Desktop, Documents, Downloads."""
    try:
        query = query.lower().strip()
        results = []

        for root_dir in SEARCH_ROOTS:
            if not os.path.exists(root_dir):
                continue

            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Skip hidden and system folders
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]

                for filename in filenames:
                    if query in filename.lower():
                        if file_type and not filename.lower().endswith(file_type.lower()):
                            continue
                        full_path = os.path.join(dirpath, filename)
                        results.append(full_path)

                        if len(results) >= max_results:
                            break
                if len(results) >= max_results:
                    break
            if len(results) >= max_results:
                break

        if not results:
            return f"No files found matching '{query}'."

        file_list = "\n".join(f"  {i+1}. {os.path.basename(f)} → {f}" for i, f in enumerate(results))
        return f"Found {len(results)} file(s):\n{file_list}"

    except Exception as e:
        log_error("search_files", e)
        return f"Search failed: {str(e)}"


def get_recent_files(folder: str = "Desktop", count: int = 10) -> str:
    """Get the most recently modified files in a folder."""
    try:
        folder_path = os.path.join(os.path.expanduser("~"), folder)
        if not os.path.exists(folder_path):
            return f"Folder '{folder}' not found."

        files = []
        for f in os.listdir(folder_path):
            full = os.path.join(folder_path, f)
            if os.path.isfile(full):
                files.append((f, os.path.getmtime(full)))

        files.sort(key=lambda x: x[1], reverse=True)
        top_files = files[:count]

        if not top_files:
            return f"No files found in {folder}."

        from datetime import datetime
        listing = "\n".join(
            f"  {i+1}. {name} (modified {datetime.fromtimestamp(mtime).strftime('%b %d, %I:%M %p')})"
            for i, (name, mtime) in enumerate(top_files)
        )
        return f"Recent files in {folder}:\n{listing}"

    except Exception as e:
        log_error("get_recent_files", e)
        return f"Failed to get recent files: {str(e)}"
