# Import Packages
import requests
from datetime import datetime, timedelta
from typing import Optional


def get_api_request(): ...


def search_news_articles(
    topic: str,
    api_key: str,
    url: str = "https://newsapi.org/v2/everything",
    language: Optional[str] = None,
    from_date: Optional[str] = None,
    sort_type: str = "relevancy",
):

    params = {
        "q": topic,
        "from": from_date if from_date else datetime.now() - timedelta(days=30),
        "sortBy": sort_type,
        "language": language,
        "apiKey": api_key,
    }

    response = requests.get(
        url,
        params=params,
    )
    articles = []

    print(response.status_code)

    match response.status_code:
        case 401:
            print(
                "Unauthorized Error: There seems to be something wrong with your API Key"
            )
            response.raise_for_status()
        case 429:
            print(
                "Too Many Requests Error: You made too many requests. Take a breather before trying again"
            )
            response.raise_for_status()
        case 500:
            print(
                "Server Error: News API is having server issues. There's not quick fix for this :("
            )
            response.raise_for_status()
        case 200:
            data = response.json()
            # print(data)
            for article in data["articles"]:
                articles.append(
                    {
                        "title": article["title"],
                        "url": article["url"],
                        "publishedAt": article["publishedAt"],
                    }
                )
        case _:
            response.raise_for_status()
    return articles


def summarize_content(content): ...
