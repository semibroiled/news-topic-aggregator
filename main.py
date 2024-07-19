import os
import csv
import pandas as pd
from datetime import datetime

# Import News Search Modules
from search_news import search_news_articles

# Import Console Animation
from utils.spinner import Spinner

# Import ENV Utils
from utils.get_keys import get_env

from enum import Enum


class ApplicationMode(Enum):
    RUN= True


def main():

    # Initialize debut settings
    NEWSAPI_KEY = get_env("NEWS_API_KEY") # Extract API Key
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
        print(f"Alright! I will the web for articles about '{topic}'")
        spinner = Spinner("Fetching articles...")
        spinner.start()
        articles = search_news_articles(topic, NEWSAPI_KEY)
        spinner.stop()

        # If no articles found, let us know some details and skip iteration
        if not articles:
            print(f"No articles found for the topic\n>>{topic}<<\nin >>{language}<<.\n")
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

if __name__ == "__main__":
    print("Starting Application...")
    main()
    print("Application closed.")
