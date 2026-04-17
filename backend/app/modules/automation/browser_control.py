import webbrowser
import urllib.parse
from app.utils.logger import log_error


# ─── Website registry ─────────────────────────────────────
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "chatgpt": "https://chat.openai.com",
    "linkedin": "https://www.linkedin.com",
    "wikipedia": "https://www.wikipedia.org",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
    "twitter": "https://x.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "gmail": "https://mail.google.com",
    "drive": "https://drive.google.com",
    "maps": "https://maps.google.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
}

# ─── Search URL templates ─────────────────────────────────
SEARCH_URLS = {
    "google": "https://www.google.com/search?q={}",
    "youtube": "https://www.youtube.com/results?search_query={}",
    "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={}",
    "github": "https://github.com/search?q={}",
    "stackoverflow": "https://stackoverflow.com/search?q={}",
    "stack overflow": "https://stackoverflow.com/search?q={}",
    "reddit": "https://www.reddit.com/search/?q={}",
    "amazon": "https://www.amazon.in/s?k={}",
}


def open_website(site_name: str) -> str:
    """Open a website by name."""
    site_name = site_name.lower().strip()

    if site_name in WEBSITES:
        webbrowser.open(WEBSITES[site_name])
        return f"Opening {site_name.title()}."

    # Fuzzy match
    for key in WEBSITES:
        if site_name in key or key in site_name:
            webbrowser.open(WEBSITES[key])
            return f"Opening {key.title()}."

    # Try as a URL
    if "." in site_name:
        url = site_name if site_name.startswith("http") else f"https://{site_name}"
        webbrowser.open(url)
        return f"Opening {site_name}."

    return f"Website '{site_name}' not found."


def search_website(query: str, platform: str = "google") -> str:
    """Search for a query on a specific platform."""
    query = query.strip()
    platform = platform.lower().strip()

    if not query:
        return "No search query provided."

    search_template = SEARCH_URLS.get(platform, SEARCH_URLS["google"])
    encoded_query = urllib.parse.quote(query)
    url = search_template.format(encoded_query)

    try:
        webbrowser.open(url)
        return f"Searching {platform.title()} for '{query}'."
    except Exception as e:
        log_error("search_website", e)
        return f"Failed to search: {str(e)}"