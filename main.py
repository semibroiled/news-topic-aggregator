import os
import csv
import pandas as pd

# Import News Search Modules
from search_news import search_news_articles

# Import Console Animation
from utils.spinner import Spinner

# Import ENV Utils
from utils.get_keys import get_env

from enum import Enum


class ApplicationMode(Enum):
    RUN_CONTINUOUSLY = True


def main():

    # Initialize debut settings
    language = "en"

    NEWSAPI_KEY = get_env("NEWS_API_KEY")

    while ApplicationMode.RUN_CONTINUOUSLY.value:
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


if __name__ == "__main__":
    print("Starting Application...")
    main()
