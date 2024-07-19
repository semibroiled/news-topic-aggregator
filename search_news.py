# Import Packages
import requests
from datetime import datetime, timedelta


def get_api_request(): ...


def search_news_articles(
    topic: str,
    api_key: str,
    sort_type: str = "relevancy",
    language="en",
):
    query = f"q={topic}"
    sort = f"&sortBy={sort_type}"
    language = f"&language={language}"
    url = f"https://newsapi.org/v2/everything?{query}&from={datetime.now() - timedelta(days=30)}{language}{sort}&apiKey={api_key}"

    response = requests.get(url)
    articles = []

    print(response.status_code)

    match response.status_code:
        case 401:
            print(
                "Unauthorized Error: There seems to be something wrong with your API Key"
            )
        case 429:
            print(
                "Too Many Requests Error: You made too many requests. Take a breather before trying again"
            )
        case 500:
            print(
                "Server Error: News API is having server issues. There's not quick fix for this :("
            )
        case 200:
            data = response.json()
            print(data)
            for article in data["articles"]:
                articles.append(
                    {
                        "title": article["title"],
                        "url": article["url"],
                        "publishedAt": article["publishedAt"],
                    }
                )
    return articles

def summarize_content(content):
    