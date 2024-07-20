"""
This module provides functions for summarizing content using a Hugging Face pipeline and extracting named entities using NLTK.

Functions:
    summarize_content_pipeline(content: str, model_id: Optional[str] = "facebook/bart-large-cnn") -> str:
        Summarizes the given content using a specified Hugging Face model.

    extract_named_entities(content: str) -> Counter[str, int]:
        Extracts named entities from the given content and returns their counts.

Example Usage:
    content = '''1. "Tech Giant Unveils Revolutionary AI Model, Promising to Transform Healthcare"
                2. "Historic Climate Agreement Reached at Global Summit, Targets Net-Zero Emissions by 2050"
                3. "Breakthrough in Renewable Energy: Scientists Develop Solar Panel with 50% Efficiency"
                4. "Local Startup Secures $10 Million Funding to Expand Sustainable Agriculture Practices"
                5. "City Council Approves Ambitious Plan for 100% Electric Public Transportation by 2030"
                6. "Groundbreaking Cancer Treatment Shows 90% Success Rate in Early Clinical Trials"'''
    
    summary = summarize_content_pipeline(content)
    print(f"Summary: {summary}")

    named_entities = extract_named_entities(content)
    for entity, freq in named_entities.most_common():
        print(f"{entity}: {freq}")
"""

# Import Relevant Packages
from langchain_huggingface import HuggingFacePipeline
import nltk
from collections import Counter

# Type Hints
from typing import Optional

# Download Language Processing Packs
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")


# Function to Summarize Content using Local Resources with Hugging Face Pipeline
def summarize_content_pipeline(
    content: str,
    model_id: Optional[str] = "facebook/bart-large-cnn",
) -> str:
    """
    Summarize the given content using a Hugging Face pipeline. This function will use local
    resources to operate.

    Args:
    content (str): The content to be summarized.
    model_id Optional(str): The model ID for the Hugging Face pipeline. Default is "facebook/bart-large-cnn".

    Returns:
    str: The summarized content.
    """
    hf_llm = HuggingFacePipeline.from_model_id(
        model_id=model_id,
        task="summarization",
        pipeline_kwargs={
            "max_length": 100,
            "min_length": 30,
            "do_sample": False,
        },
    )
    summary = hf_llm.invoke(content)
    return summary


# Extract Named Entities using NLTK Packs and Tokenization
def extract_named_entities(content: str) -> Counter[str, int]:
    """
    Extract named entities from the given content using NLTK.

    Args:
    content (str): The content from which to extract named entities.

    Returns:
    Counter[str, int]: A dictionary of named entities and their counts.
    """
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


# Example Usage:
if __name__ == "__main__":
    content = """	1.	“Tech Giant Unveils Revolutionary AI Model, Promising to Transform Healthcare”
	2.	“Historic Climate Agreement Reached at Global Summit, Targets Net-Zero Emissions by 2050”
	3.	“Breakthrough in Renewable Energy: Scientists Develop Solar Panel with 50% Efficiency”
	4.	“Local Startup Secures $10 Million Funding to Expand Sustainable Agriculture Practices”
	5.	“City Council Approves Ambitious Plan for 100% Electric Public Transportation by 2030”
	6.	“Groundbreaking Cancer Treatment Shows 90% Success Rate in Early Clinical Trials”"""
    summary = summarize_content_pipeline(content)
    print(f"Summary: {summary}\n")
    print("Named Entities:\n")
    named_entities = extract_named_entities(content)
    for entity, freq in named_entities.most_common():
        print(f"{entity}: {freq}")
