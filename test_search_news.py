import pytest
import requests
from search_news import search_news_articles
from search_news import summarize_content, extract_named_entities

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

def test_extract_named_entities():
    text = "Amitav Chris Mostafa is applying to Summetix for a job. Johannes Daxenberger is going to interview him"
    named_entities = extract_named_entities(text)
    assert "Amitav Chris Mostafa" in named_entities
    assert "Johannes Daxenberger" in named_entities
    assert "Summetix" in named_entities

def test_summarize_content(monkeypatch):
    class MockSummarizer:
        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, content):
            return [{"summary_text": "This is a summary"}]
        
    monkeypatch.setattr("transformers.pipeline", MockSummarizer)

    content = "This is a form of content that is very engaging and intersting"
    summary = summarize_content(content)
    assert summary == "This is a summary"

if __name__ =="__main__":
    pytest.main()