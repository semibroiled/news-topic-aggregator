"""
summarize_content.py

This module provides functions for summarizing content using a Hugging Face pipeline and extracting named entities using NLTK.

Functions:
    - summarize_content_pipeline: Summarizes the given content using a specified Hugging Face model.
    - extract_named_entities_nltk: Extracts named entities from the given content using NLTK.

Example Usage:
    content = '''1. "Tech Giant Unveils Revolutionary AI Model, Promising to Transform Healthcare"
                2. "Historic Climate Agreement Reached at Global Summit, Targets Net-Zero Emissions by 2050"
                3. "Breakthrough in Renewable Energy: Scientists Develop Solar Panel with 50% Efficiency"
                4. "Local Startup Secures $10 Million Funding to Expand Sustainable Agriculture Practices"
                5. "City Council Approves Ambitious Plan for 100% Electric Public Transportation by 2030"
                6. "Groundbreaking Cancer Treatment Shows 90% Success Rate in Early Clinical Trials"'''
    
    summary = summarize_content_pipeline(content)
    print(f"Summary: {summary}")

    named_entities = extract_named_entities_nltk(content)
    for entity, freq in named_entities.most_common():
        print(f"{entity}: {freq}")
"""

# Import Relevant Packages
from langchain_huggingface import HuggingFacePipeline

import nltk  # type: ignore[import-untyped]

# import spacy
from collections import Counter

# Type Hints
from src.search_news import Language

# Import Enum
from enum import Enum

# Download Language Processing Packs
# For NLTK
try:
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("maxent_ne_chunker")
    nltk.download("words")
except Exception as e:
    print("Could not load NLTK packages")
    print(f"{e}")

# For Spacy
# try:
#     nlp_en = spacy.load("en_core_web_lg")
#     nlp_de = spacy.load("de_core_news_lg")  # python -m spacy download de_core_news_lg
# except Exception as e:
#     print("Could not load spacy packages")
#     print(f"{e}")


# Define Descriptive Constants
class EntityTypes(Enum):
    PERSON = "PERSON"
    ORGANIZATION = "ORG"
    GEOPOLITICAL = "GPE"
    LOCATION = "LOC"


# Function to Summarize Content using Local Resources with Hugging Face Pipeline
def summarize_content_pipeline(
    content: str,
    model_id: str = "facebook/bart-large-cnn",
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
def extract_named_entities_nltk(content: str) -> Counter:
    """
    Extract named entities from the given content using NLTK.

    Args:
        content (str): The content from which to extract named entities.

    Returns:
        Counter: A dictionary of named entities and their counts.
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


# Extract Named Entities using Statistical SpaCy Models
# def extract_named_entities_spacy(
#     text: str,
#     *,
#     language: Language,
# ) -> Counter:
#     """
#     Extract named entities from the given text using spaCy.

#     Args:
#     text (str): The text from which to extract named entities.
#     language (str): The language of the text ("en" for English, "de" for German).

#     Returns:
#     Counter: A counter of named entities and their counts.
#     """
#     match language:
#         case "en":
#             doc = nlp_en(text)
#         case "de":
#             doc = nlp_de(text)
#         case _:
#             raise ValueError(
#                 "Unsupported language. Please use 'en' for English or 'de' for German."
#             )

#     entities = [
#         ent.text
#         for ent in doc.ents
#         if ent.label_ in {entity.value for entity in EntityTypes}
#     ]
#     return Counter(entities)


# Example Usage:
if __name__ == "__main__":
    content = """	
    1.	“Tech Giant Unveils Revolutionary AI Model, Promising to Transform Healthcare”
	2.	“Historic Climate Agreement Reached at Global Summit, Targets Net-Zero Emissions by 2050”
	3.	“Breakthrough in Renewable Energy: Scientists Develop Solar Panel with 50% Efficiency”
	4.	“Local Startup Secures $10 Million Funding to Expand Sustainable Agriculture Practices”
	5.	“City Council Approves Ambitious Plan for 100% Electric Public Transportation by 2030 Sirius”
	6.	“Groundbreaking Cancer Treatment Shows 90% Success Rate in Early Clinical Trials
    7.  "Barack Obama was born in Hawaii. He was elected president in 2008.", """

    content_de = """
        1. „Technologieriese stellt revolutionäres KI-Modell vor, das das Gesundheitswesen transformieren soll“
    2. „Historisches Klimaabkommen auf globalem Gipfel erreicht, Ziel: Netto-Null-Emissionen bis 2050“
    3. „Durchbruch in der erneuerbaren Energie: Wissenschaftler entwickeln Solarpanel mit 50 % Effizienz“
    4. „Lokales Startup sichert sich 10 Millionen Dollar Finanzierung zur Erweiterung nachhaltiger Landwirtschaftspraktiken“
    5. „Stadtrat genehmigt ehrgeizigen Plan für 100 % elektrische öffentliche Verkehrsmittel bis 2030 Sirius“
    6. „Bahnbrechende Krebstherapie zeigt 90 % Erfolgsquote in frühen klinischen Studien“
    7. „Barack Obama wurde in Hawaii geboren. Er wurde 2008 zum Präsidenten gewählt.“
    8.  "Angela Merkel wurde in Hamburg geboren. Sie wurde 2005 zur Bundeskanzlerin gewählt."
    """

    # Use Example Summarizer
    summary = summarize_content_pipeline(content)
    print(f"\nSummary: {summary}")

    # Use Example NER
    # Using NLTK
    print("\nNamed Entities:")
    print("\nNLTK EN Content:")
    named_entities = extract_named_entities_nltk(content)
    for entity, freq in named_entities.most_common():
        print(f"{entity}: {freq}")

    print("\nNLTK DE Content:")
    named_entities = extract_named_entities_nltk(content_de)
    for entity, freq in named_entities.most_common():
        print(f"{entity}: {freq}")

    # Using Spacy
    # print("\nSpacy Approach EN Model EN Content:")
    # named_entities = extract_named_entities_spacy(
    #     content,
    #     language="en",
    # )
    # for entity, freq in named_entities.most_common():
    #     print(f"{entity}: {freq}")

    # print("\nSpacy Approach DE Model EN Content:")
    # named_entities = extract_named_entities_spacy(
    #     content,
    #     language="de",
    # )
    # for entity, freq in named_entities.most_common():
    #     print(f"{entity}: {freq}")

    # print("\nSpacy Approach EN Model DE Content:")
    # named_entities = extract_named_entities_spacy(
    #     content_de,
    #     language="en",
    # )
    # for entity, freq in named_entities.most_common():
    #     print(f"{entity}: {freq}")

    # print("\nSpacy Approach DE Model DE Content:")
    # named_entities = extract_named_entities_spacy(
    #     content_de,
    #     language="de",
    # )
    # for entity, freq in named_entities.most_common():
    #     print(f"{entity}: {freq}")
