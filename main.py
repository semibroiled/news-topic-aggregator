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
            "What topic would you like to search?\nType 'help' to get more assistance\nType 'exit' or 'quit' to close application\n>>"
        )
        if topic.strip().lower() == ("exit" or "quit"):
            break
        if topic.strip().lower() == "help":
            print(f"Not yet implemented\n")
            continue
        if topic.strip().lower() == "!setlang":
            language = (
                input(
                    "Restrict your output to a specific language\nType 'en' for English or 'de' for German and press Enter\n>>"
                )
                .strip()
                .lower()
            )
            print(f"Language is set to {language}\n")
            continue

        print(f"Alright! I will the web for articles about '{topic}'")

        spinner = Spinner("Fetching articles...")
        spinner.start()

        articles = search_news_articles(topic, NEWSAPI_KEY)

        spinner.stop()

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
