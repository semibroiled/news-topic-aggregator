# Import Relevant Packages
import pandas as pd  # type: ignore[import-untyped]
import time
from datetime import datetime
from pathlib import Path
import yaml, re  # type: ignore[import-untyped]
from tabulate import tabulate  # type: ignore[import-untyped]
from collections import Counter

# Import News Search Modules
from src.search_news import search_news_articles

# Import Summarization Modules
from src.summarize_content import (
    summarize_content_pipeline,
    extract_named_entities_nltk,
)

# Import Console Animation
from src.utils.spinner import Spinner

# Import ENV Utils
from src.utils.get_keys import get_env

# Import Input Cleaner
from src.utils.secure_input import sanitize_input

# Import Help Strings
from src.cli_help import help_command_output

# Import Enum for Descriptive Constants
from enum import Enum


# Set Descriptive Constants
class ApplicationMode(Enum):
    RUN = True


# Main Script for CLI Application
def main():

    # Initialize debut settings
    NEWS_API_KEY = get_env("NEWS_API_KEY")  # Extract API Key for NewsAPI
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    language = config["default_language"]  # Default to English
    # Usage Hints
    print(
        "\nEnter a topic to search. Or..\n"
        "Type '!help' to get usage instructions\n"
        "Type '!setlang' to change query language\n"
        "Type '!exit' or '!quit' to close application"
    )

    # * Run Application
    while ApplicationMode.RUN.value:
        # * Topic Prompt
        topic = input("\nWhat topic would you like to search?\n" ">>")

        topic = sanitize_input(topic)

        # * Guard Clauses to treat input flags
        # - Coerce some kind of input
        if topic == "":
            print("\nWARNING: You need to type something to search")
            continue
        # - Exit Application
        if topic.strip().lower() in ("!exit", "!quit"):
            break
        # - Help String
        if topic.strip().lower() == "!help":
            print(help_command_output())
            continue
        # - Change Language
        if topic.strip().lower() == "!setlang":
            language = (
                input(
                    "Restrict your output to a specific language\n"
                    "Type 'en' for English or 'de' for German and press Enter\n"
                    f"Current Language Setting: {language}\n"
                    ">>"
                )
                .strip()
                .lower()
            )
            language = sanitize_input(language)
            print(f"Language is set to >>{language}<<")
            match language:
                case "de":
                    continue
                case "en":
                    continue
                case _:
                    print("This is not a valid setting. Switching to Default.")
                    language = "en"
                    continue
        # Search Articles from News API
        print(f"\nAlright! Searching for articles about >>{topic}<<")

        with Spinner("Fetching Articles..."):
            try:
                articles = search_news_articles(
                    topic,
                    NEWS_API_KEY,
                    language=language,
                )
            except Exception as e:
                print(f"\n{e}")
                print("\nPlease Try Again")
                continue

        # If no articles found, let us know some details and skip iteration
        if not articles:
            print(
                f"No articles found.\nTopic >>{topic}<<\nLanguage >>{language}<<.\n\n"
            )
            continue

        # Remove deleted articles
        with Spinner("Filtering removed articles..."):
            time.sleep(3)
            filtered_articles = [
                article for article in articles if not "remove" in article["url"]
            ]

        # * Requirement 1: Save Articles as a CSV file right after search
        with Spinner("Saving articles locally..."):
            df_articles = pd.DataFrame(filtered_articles)
            # Define the destination path
            destination_path = Path(config["output"]["folder"])

            # Create a folder for the output if it doesn't exist
            if not destination_path.exists():
                print(f"Path:('{destination_path}') not found")
                print(f"Making '{destination_path}'")
                destination_path.mkdir(parents=True, exist_ok=True)
            # Set Filename and Save Path; Save File from df to CSV
            topic_alnum = re.sub(
                r"[^a-zA-Z0-9\s]", "", topic
            )  # Remove any speicals chars to avoid save issues
            topic_alnum = topic_alnum.replace(" ", "_")
            csv_filename = f"{str(topic_alnum).lower()}_articles_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            save_file = destination_path / csv_filename
            df_articles.to_csv(save_file, index=False)
        print(f"\nAll articles saved to Path('{save_file}') ✅")

        # * Requirement 2: Print Top 15 Articles in Terminal by Sorting Relevance
        # Reset Index to begin at 1
        df_articles.index = df_articles.index + 1
        # Set pandas display options to show all columns and full width
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)

        # Print the first 15 rows of the filtered DataFrame using tabulate for better formatting
        print("\n##########################Top 15 Articles##########################")
        print(
            tabulate(
                df_articles.head(15), headers="keys", tablefmt="grid", showindex=True
            )
        )

        # * Requirement 3: Summarize Headlines of Top 15  Articles
        with Spinner("Summarizing Headlines..."):
            summary = summarize_content_pipeline(
                "\n".join([article["title"] for article in filtered_articles[:15]])
            )

        print("\n*--Summary of Top 15 Articles Headlines--*")
        print(summary)

        # * Requirement 4: List Named Entities in Descending Order
        with Spinner("Listing Named Entities..."):
            time.sleep(3)
            all_named_entities = []  # Empty list to store entities
            for title in df_articles.head(15)["title"]:
                named_entities = extract_named_entities_nltk(title)
                all_named_entities.extend(named_entities)
            named_entities_counter = Counter(all_named_entities)
        print("\n*--Named Entities in Top 15 Articles Headlines--*")
        for entity, freq in named_entities_counter.most_common():
            print(f"{entity}: {freq}")


if __name__ == "__main__":
    print("\nStarting Application...")
    main()
    print("Application closed.")
