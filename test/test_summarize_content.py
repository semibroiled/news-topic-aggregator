import pytest
from src.summarize_content import extract_named_entities, summarize_content_pipeline


def test_extract_named_entities():
    text = "Amitav Chris Mostafa is applying to Summetix for a job. Johannes Daxenberger is going to interview him"
    named_entities = extract_named_entities(text)
    assert "Amitav Chris Mostafa" in named_entities
    assert "Johannes Daxenberger" in named_entities
    assert "Summetix" in named_entities
    assert "applying" not in named_entities


def test_summarize_content(monkeypatch):
    class MockSummarizer:
        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return [{"summary_text": "This is a summary"}]

    monkeypatch.setattr("langchain_huggingface.HuggingFacePipeline", MockSummarizer)

    content = "This is a longform content that serves solely to mock unittest a reusable function. The goal is to see if we get a sensible output that is shorter version of the content here whilst still containing the most important information"
    summary = summarize_content_pipeline(content)
    assert len(summary) < len(content)


if __name__ == "__main__":
    pytest.main()
