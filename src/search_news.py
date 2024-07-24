"""
search_news.py

This module provides a function to search for news articles using the News API.

Functions:
    - search_news_articles: Searches for news articles related to the given topic using the News API and returns a list of articles.

Example Usage:
    api_key = "your_news_api_key"
    topic = "technology"
    articles = search_news_articles(topic, api_key)
    for article in articles:
        print(f"Title: {article['title']}, URL: {article['url']}, Published At: {article['publishedAt']}")
"""

# Import Relevant Packages
import requests  # type: ignore[import-untyped]
from datetime import datetime, timedelta
from src.utils.get_keys import get_env

# Type Hints
from typing import Optional, List, Dict
from typing import Literal, TypeAlias

# Type Aliases
Language: TypeAlias = Literal["en", "de"]


def search_news_articles(
    topic: str,
    api_key: Optional[str],
    *,
    language: Optional[Language] = "en",
    url: Optional[str] = "https://newsapi.org/v2/everything",
    from_date: Optional[datetime] = None,
    sort_type: Optional[str] = "relevancy",
) -> List[Dict[str, str]]:
    """
    Search for news articles related to the given topic using the News API.

    Args:
        topic (str): The topic to search for.
        api_key (str): Your News API key.
        url (Optional[str]): The URL endpoint for the News API. Default is "https://newsapi.org/v2/everything".
        language (Optional[Language]): The language of the news articles. Can only be en for English or de for German.
        from_date (Optional[datetime]): The start date for the news articles (format: YYYY-MM-DD).
        sort_type (Optional[str]): The sort type for the news articles. Default is "relevancy".

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the title, URL, and publication date of the articles.

    Raises:
        AssertionError: If no API key is provided.
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    assert (
        api_key
    ), "There are no API Key passed to function\n\
        Consult README on how to set .env up properly"

    # Default to Last Month if No From Date Passed
    # if not from_date:
    #     from_date = datetime.now() - timedelta(
    #         days=30
    #     )

    # Set Params
    params = {
        "q": topic,
        "from": from_date,
        "sortBy": sort_type,
        "language": language,
        "apiKey": api_key,
    }

    # Make GET Request
    response = requests.get(
        url,
        params=params,
    )

    # Initialize Empty List to Store Articles
    articles = []

    # print(response.status_code)

    # Conditionally Treat Different Status Codes
    match response.status_code:
        case 200:
            data = response.json()
            # print(data)
            for article in data.get("articles", []):
                articles.append(
                    {
                        "title": article["title"],
                        "url": article["url"],
                        "publishedAt": article["publishedAt"],
                    }
                )
        case _:
            print("\n")
            response.raise_for_status()
            print("Use command !help to get instruction on how to search")
            print("If the API itself is overburdened, wait before trying again")
    return articles


# Example Usage:
if __name__ == "__main__":
    api_key: Optional[str] = get_env("NEWS_API_KEY")
    topic = "technology"
    articles = search_news_articles(topic, api_key, language="de")
    for article in articles:
        print(
            f"Title: {article['title']}, URL: {article['url']}, Published At: {article['publishedAt']}"
        )
