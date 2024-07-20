import os
import csv
import pandas as pd
from datetime import datetime

# Import News Search Modules
from search_news import search_news_articles

# Import Summarization Modules
from search_news import summarize_content_pipeline, extract_named_entities
#from getpass import getpass

# Import Console Animation
from utils.spinner import Spinner

# Import ENV Utils
from utils.get_keys import get_env

from enum import Enum


class ApplicationMode(Enum):
    RUN= True


def main():

    # Initialize debut settings
    NEWS_API_KEY = get_env("NEWS_API_KEY") # Extract API Key for NewsAPI
    #HUGGINGFACEHUB_API_KEY = getpass() # Extract API Key for HF
    #os.environ["HUGGINGFACEHUB_API_KEY"] = HUGGINGFACEHUB_API_KEY
    HUGGING_FACE_API_KEY = get_env("HUGGING_FACE_API_KEY")
    language = None

    # Run Application
    while ApplicationMode.RUN.value:
        topic = input(
            "What topic would you like to search?\n"\
            "Type 'help' to get usage instructions\n"\
            "Type 'exit' or 'quit' to close application\n"\
            ">>"
        )

        # Guard Clauses to treat input flags
        # Coerce some kind of input
        if topic == "":
            print("\nWARNING: You need to type something to search\n")
            continue
        # Exit Application
        if topic.strip().lower() == ("exit" or "quit"):
            break
        # Help String
        if topic.strip().lower() == "help":
            print(f"- Language Setting\n\t-- Use command '!setlang' on prompt to change query language\n"\
                "- Advanced Queries\n"\
                "\t--Put your topic in quotation marks for exact match. (eg: \"elon musk\")\n"\
                "\t--Use '+' and '-' to specify which keywords must or must not appear. (eg: gamestop +stonks -sell)\n"\
                "\t--Use Boolean Operators. (eg: (crypto AND bitcoin) NOT ethereum)\n"\
                "\t--Limit search to titles or content . (eg: InTitle=\"title search\")\n")
            continue
        # Change Language
        if topic.strip().lower() == "!setlang":
            language = (
                input(
                    "Restrict your output to a specific language\n"\
                    "Type 'en' for English or 'de' for German and press Enter\n"\
                    ">>"
                )
                .strip()
                .lower()
            )
            print(f"Language is set to >>{language}<<\n")
            continue

        # Search Articles from News API
        print(f"Alright! I will search the web for articles about '{topic}'")
        spinner = Spinner("Fetching articles...")
        spinner.start()
        articles = search_news_articles(topic, NEWS_API_KEY)
        spinner.stop()

        # If no articles found, let us know some details and skip iteration
        if not articles:
            print(f"No articles found.\nTopic >>{topic}<<\nLanguage >>{language}<<.\n")
            continue
        
        # Requirement 1: Print Top 15 Articles by Sort
        print("Top 15 Articles:")

        for i, article in enumerate(articles[:15]):
            print(f"{i+1} -> {article["title"]} ({article["publishedAt"]}) - {article["url"]}")

        # Requirement 2: Save Articles as a CSV file
        df_articles = pd.DataFrame(articles)
        csv_filename = f"history/{topic.replace(" ", "_")}_articles_{language}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"
        df_articles.to_csv(csv_filename, index=False)
        print(f"All articles saved to {csv_filename} in history subfolder\n")

        summary = summarize_content_pipeline("\n".join([article["title"] for article in articles[:15]]))

        named_entities = extract_named_entities("\n".join(article["title"] for article in articles[:15] ))

        print("*--Summary of Top 15 Articles Headlines--*")
        print(summary)

        print("\n")

        print("*--Named Entities in Top 15 Articles Headlines--*")
        for entity, freq in named_entities.most_common():
            print(f"{entity}: {freq}")
        
        print("\n")

if __name__ == "__main__":
    print("Starting Application...")
    main()
    print("Application closed.")
