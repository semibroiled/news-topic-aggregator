import pytest
import requests
from search_news import search_news_articles


@pytest.fixture
def mock_requests(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            match self.status_code:
                case 401:
                    raise requests.exceptions.HTTPError(f"{self.status_code} Error: Mock error for testing")
                case 429:
                    raise requests.exceptions.HTTPError(f"{self.status_code} Error: Mock error for testing")
                case 500:
                    raise requests.exceptions.HTTPError(f"{self.status_code} Error: Mock error for testing")
                case _:
                    print("No Test Case Implemented for this code")
    
    def mock_get(url, **kwargs):
        params = kwargs.get("params", {})
        match params.get("q"):
            case "test":
                return MockResponse(
                    {
                        "articles": [
                            {
                                "title": "Test Article",
                                "url": "http://test.test",
                                "publishedAt": "2024-07-19T12:34:56Z",
                            }
                        ]
                    },
                    200,
                )
            case "rate_limit":
                return MockResponse({}, 429)
            case "unauthorized":
                return MockResponse({}, 401)
            case "server_error":
                return MockResponse({}, 500)
            case _:
                raise requests.exceptions.RequestException("Network Error")

    monkeypatch.setattr(requests, "get", mock_get)


def test_search_news_articles_success(mock_requests):
    articles = search_news_articles("test", "dummy")
    assert len(articles) == 1
    assert articles[0]["title"] == "Test Article"
    assert articles[0]["url"] == "http://test.test"
    assert articles[0]["publishedAt"] == "2024-07-19T12:34:56Z"


def test_search_news_articles_rate_limit(mock_requests):
    with pytest.raises(requests.exceptions.HTTPError):
        search_news_articles("rate_limit", "dummy_api_key")


def test_search_news_articles_unauthorized(mock_requests):
    with pytest.raises(requests.exceptions.HTTPError):
        search_news_articles("unauthorized", "dummy_api_key")


def test_search_news_articles_server_error(mock_requests):
    with pytest.raises(requests.exceptions.HTTPError):
        search_news_articles("server_error", "dummy_api_key")


def test_search_news_articles_network_error(mock_requests):
    with pytest.raises(requests.exceptions.RequestException):
        search_news_articles("network_error", "dummy_api_key")
