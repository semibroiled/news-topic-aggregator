"""
This module provides a function to search for news articles using the News API.

Functions:
    search_news_articles(
        topic: str,
        api_key: str,
        url: Optional[str] = "https://newsapi.org/v2/everything",
        language: Optional[str] = None,
        from_date: Optional[str] = None,
        sort_type: Optional[str] = "relevancy",
    ) -> List[Dict[str, str]]:
        Searches for news articles related to the given topic using the News API and returns a list of articles.

Example Usage:
    api_key = "your_news_api_key"
    topic = "technology"
    articles = search_news_articles(topic, api_key)
    for article in articles:
        print(f"Title: {article['title']}, URL: {article['url']}, Published At: {article['publishedAt']}")
"""

# Import Relevant Packages
import requests
from datetime import datetime, timedelta
from src.utils.get_keys import get_env

# Type Hints
from typing import Optional, List, Dict


def search_news_articles(
    topic: str,
    api_key: str,
    url: Optional[str] = "https://newsapi.org/v2/everything",
    language: Optional[str] = None,
    from_date: Optional[str] = None,
    sort_type: Optional[str] = "relevancy",
) -> List[Dict[str, str]]:
    """
    Search for news articles related to the given topic using the News API.

    Args:
    topic (str): The topic to search for.
    api_key (str): Your News API key.
    url (Optional[str]): The URL endpoint for the News API. Default is "https://newsapi.org/v2/everything".
    language (Optional[str]): The language of the news articles.
    from_date (Optional[str]): The start date for the news articles (format: YYYY-MM-DD). Default is 30 days ago.
    sort_type (Optional[str]): The sort type for the news articles. Default is "relevancy".

    Returns:
    List[Dict[str, str]]: A list of dictionaries containing the title, URL, and publication date of the articles.
    """
    if not from_date:
        from_date = datetime.now() - timedelta(
            days=30
        )  # Default to Last Month if No From Date Passed

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

    # Conditionally Treat Different Status Code
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
            for article in data.get("articles", []):
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


# Example Usage:
if __name__ == "__main__":
    api_key = get_env("NEWS_API_KEY")
    topic = "technology"
    articles = search_news_articles(topic, api_key)
    for article in articles:
        print(
            f"Title: {article['title']}, URL: {article['url']}, Published At: {article['publishedAt']}"
        )