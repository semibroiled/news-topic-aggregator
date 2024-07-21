# Import Relevant Packages
import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml

# Import News Search Modules
from src.search_news import search_news_articles

# Import Summarization Modules
from src.summarize_content import summarize_content_pipeline, extract_named_entities

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
    RUN= True

# Main Script for CLI Application
def main():

    # Initialize debut settings
    NEWS_API_KEY = get_env("NEWS_API_KEY") # Extract API Key for NewsAPI
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    language = config["default_language"] # Default to English 
    # Usage Hints
    print("\nEnter a topic to search. Or..\n"
        "Type '!help' to get usage instructions\n"
        "Type '!setlang' to change query language\n"
        "Type '!exit' or '!quit' to close application")

    # Run Application
    while ApplicationMode.RUN.value:
        # Topic Prompt
        topic = input(
            "\nWhat topic would you like to search?\n"\
            ">>"
        )

        topic = sanitize_input(topic)

        # Guard Clauses to treat input flags
        # Coerce some kind of input
        if topic == "":
            print("\nWARNING: You need to type something to search")
            continue
        # Exit Application
        if topic.strip().lower() in ("!exit", "!quit"):
            break
        # Help String
        if topic.strip().lower() == "!help":
            print(help_command_output())
            continue
        # Change Language
        if topic.strip().lower() == "!setlang":
            language = (
                input(
                    "Restrict your output to a specific language\n"\
                    "Type 'en' for English or 'de' for German and press Enter\n"\
                    f"Current Language Setting: {language}\n"\
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
                    language = "en"
                    print("This is not a valid setting. Switching to Default.")
                    continue    
        # Search Articles from News API
        print(f"\nAlright! I will search the web for articles about '{topic}'")
        
        
        with Spinner("Fetching Articles..."):
            try:
                articles = search_news_articles(topic, NEWS_API_KEY)
            except Exception as e:
                print(e)
                continue

        # If no articles found, let us know some details and skip iteration
        if not articles:
            print(f"No articles found.\nTopic >>{topic}<<\nLanguage >>{language}<<.\n\n")
            continue
        
        # Requirement 1: Print Top 15 Articles by Sorting Relevance
        print("\n########Top 15 Articles########")

        for i, article in enumerate(articles[:15]):
            print(f"{i+1} -> {article["title"]} ({article["publishedAt"]}) - {article["url"]}")
        
        # Requirement 2: Save Articles as a CSV file
        df_articles = pd.DataFrame(articles)
        
        # Define the destination path
        destination_path = Path(config["output"]["folder"])

        # Create a folder for the output if it doesn't exist
        if not destination_path.exists():
            print(f"Path:('{destination_path}') not found")
            print(f"Making '{destination_path}'")
            destination_path.mkdir(parents=True, exist_ok=True)
        # Set Filename and Save Path; Save File from df to CSV
        csv_filename = f"{topic.replace(" ", "_")}_articles_{language}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"
        save_file = destination_path / csv_filename
        df_articles.to_csv(save_file, index=False)
        print(f"\nAll articles saved to Path('{save_file}') in {destination_path} subfolder")
        
        # Requirement 3: Summarize Headlines of Top 15  Articles
        print("\n")
        with Spinner("Summarizing Headlines..."):
            summary = summarize_content_pipeline("\n".join([article["title"] for article in articles[:15]]))
            
        print("\n*--Summary of Top 15 Articles Headlines--*")
        print(summary)

        # Requirement 4: List Named Entities in Descending Order
        with Spinner("Listing Named Entities..."):
            named_entities = extract_named_entities("\n".join(article["title"] for article in articles[:15] ))
        #print("\n")
        print("\n*--Named Entities in Top 15 Articles Headlines--*")
        for entity, freq in named_entities.most_common():
            print(f"{entity}: {freq}")

if __name__ == "__main__":
    print("\nStarting Application...")
    main()
    print("Application closed.")
