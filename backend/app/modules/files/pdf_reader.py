import os
from app.utils.logger import log_error


def read_pdf(filepath: str, max_pages: int = 5) -> str:
    """
    Read text content from a PDF file.
    Requires PyPDF2 (pip install PyPDF2).
    """
    try:
        if not os.path.exists(filepath):
            return f"PDF not found: {filepath}"

        if not filepath.lower().endswith('.pdf'):
            return "Not a PDF file."

        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return "PDF reading requires PyPDF2. Install it with: pip install PyPDF2"

        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        pages_to_read = min(max_pages, total_pages)

        text = []
        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text.append(f"--- Page {i+1} ---\n{page_text.strip()}")

        if not text:
            return "Couldn't extract text from this PDF. It may be image-based."

        result = "\n\n".join(text)
        if total_pages > pages_to_read:
            result += f"\n\n... ({total_pages - pages_to_read} more pages not shown)"

        return result

    except Exception as e:
        log_error("read_pdf", e)
        return f"Failed to read PDF: {str(e)}"


def get_pdf_info(filepath: str) -> str:
    """Get info about a PDF file."""
    try:
        if not os.path.exists(filepath):
            return f"PDF not found: {filepath}"

        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return "PDF reading requires PyPDF2. Install with: pip install PyPDF2"

        reader = PdfReader(filepath)
        info = reader.metadata

        size_kb = round(os.path.getsize(filepath) / 1024, 1)
        pages = len(reader.pages)

        details = f"PDF: {os.path.basename(filepath)}\n"
        details += f"  Pages: {pages}\n"
        details += f"  Size: {size_kb} KB\n"

        if info:
            if info.title:
                details += f"  Title: {info.title}\n"
            if info.author:
                details += f"  Author: {info.author}\n"

        return details

    except Exception as e:
        log_error("get_pdf_info", e)
        return f"Failed to get PDF info: {str(e)}"
