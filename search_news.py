# Import Packages
import requests
from datetime import datetime, timedelta
from typing import Optional

from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import nltk
from collections import Counter


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


# Define a Prompt Template for Summary
summarization_template = PromptTemplate(
    input_variables=["content"],
    template="Make a succint summary of the following content: \n{content}\nSummary:",
)

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")


def summarize_content(content):
    hf_llm = HuggingFaceEndpoint(model_name="facebook/bart-large-cnn")
    summarize_chain = LLMChain(llm=hf_llm, prompt=summarize_content)
    summary = summarize_chain.run({"content": content})
    return summary


def extract_named_entities(content):
    sentences = nltk.sent_tokenize(content)
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    pos_tags = [nltk.pos_tag(token) for token in tokens]
    chunks = [nltk.ne_chunk(tag) for tag in pos_tags]

    named_entities = []
    for chunk in chunks:
        current_chunk = []
        for tree in chunk:
            if hasattr(tree, "label"):
                current_chunk.append(" ".join([child[0] for child in tree]))
            elif current_chunk:
                named_entities.append(" ".join(current_chunk))
                current_chunk = []
        if current_chunk:
            named_entities.append(" ".join(current_chunk))

    return Counter(named_entities)
