import requests
import time
from app.utils.logger import log_error

_news_cache = {"data": None, "time": 0}
CACHE_TTL = 1800  # 30 minutes

def get_news() -> str:
    """
    Get top news headlines using a free RSS-to-JSON service.
    Uses Google News RSS feed via rss2json.
    Caches the results for 30 minutes.
    """
    now = time.time()
    if _news_cache["data"] and (now - _news_cache["time"] < CACHE_TTL):
        return _news_cache["data"]

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

            result = "Here are the top headlines:\n" + "\n".join(headlines)
            _news_cache["data"] = result
            _news_cache["time"] = now
            return result

        return "Couldn't fetch news right now."

    except Exception as e:
        log_error("get_news", e)
        return "News service is unavailable at the moment."
