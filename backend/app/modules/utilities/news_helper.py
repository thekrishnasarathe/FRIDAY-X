import requests
from app.utils.logger import log_error


def get_news() -> str:
    """
    Get top news headlines using a free RSS-to-JSON service.
    Uses Google News RSS feed via rss2json.
    """
    try:
        url = "https://rss.app/feeds/v1.1/ts4rGQD7HPZOOQ3r.json"
        # Fallback: Google News RSS
        fallback_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

        response = requests.get(
            "https://api.rss2json.com/v1/api.json",
            params={"rss_url": fallback_url, "count": 5},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])[:5]

            if not items:
                return "No news available right now."

            headlines = []
            for i, item in enumerate(items, 1):
                title = item.get("title", "Untitled")
                headlines.append(f"{i}. {title}")

            return "Here are the top headlines:\n" + "\n".join(headlines)

        return "Couldn't fetch news right now."

    except Exception as e:
        log_error("get_news", e)
        return "News service is unavailable at the moment."
