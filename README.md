# News Topic Aggregator

This project is a CLI Apllication that searches for recent news articles on a given topic and generates a summary of the top articles

## Installation

1. Clone the repository: 
   => ```sh git clone link-to-repository```
2. Enter cloned directory
    => `cd news-topic-aggregator`

3. Create Virtual Environment
    => Make sure you have Python installed. Python 3.12 is reccomennded
    => `python3 -m venv .venv`

4. Activate the Virtual Environment
    => `source .venv/bin/activate`

5. Verify you are in the correct envrironment
    => `which pip` and `which python` to check if you're in .venv

6. Install required packages
    => `pip install -r requirements.txt`

## Usage

Run the application in your terminal.

`python src/main.py`

If you're getting Import Errors such as no module named 'src'; update PYTHONPATH and then run `main.py`

```sh
export PYTHONPATH="${PYTHONPATH}:/path/to/project_root/src"
python src/main.py
```

## Run Unit Tests

To run tests, from the project directory in terminal use command:
1. => `pytest`
2. or =>`pytest -v` for detailed output in verbose mode
3. => `pytest -s` to show print statements
4. => `pytest -x` to stop after first FAIL

5. Run pytest for a specific file
 => `pytest path/to/test_file.py`

6. Run specific test within a file
=> `pytest path/to/test_file.py::test_case_name`

## Configuring .env

Rename the `.env.example` file to `.env`

Enter your API Key for News API instead of the example listed.

## Running in Docker

To Run in Docker, you need to have Docker Desktop installed and running in the background. From your repository, use

1. `docker build -t news-topic-aggregator .`
2. `docker run -it --rm --env-file .env news-topic-aggregator`

## Setting up News API Token

1. Make an account at https://newsapi.org/
2. Press **Get API Key->** Button on Homepage
3. You will be offered a free development API Key. Be sure to save it and use it

## Navigating the Application

Upon running the application, you will be prompted to enter a topic to search. You can also use the following commands:

- !help - Display usage instructions.
- !setlang - Change query language.
- !exit or !quit - Close the application.
 
### Language Settings

To change the query language, use the !setlang command. Type en for English or de for German.

Application Defaults to English.

### Application Settings

Type !exit or !quit to close the application.

### Advanced Queries

	•	Exact Match: Use quotation marks for exact matches, e.g., "elon musk".
	•	Mandatory/Excluded Keywords: Use + and - to specify mandatory and excluded keywords, e.g., gamestop +stonks -sell.
	•	Boolean Operators: Use Boolean operators for complex queries, e.g., (crypto AND bitcoin) NOT ethereum.
	•	Title-Specific Search: Limit search to titles using InTitle="title search".


## Project Structure

```sh
news-topic-aggregator/
├── .venv/
├── history/
├── src/
│   ├── utils/
│   │   ├── get_keys.py
│   │   ├── spinner.py
│   │   └── __init__.py
│   ├── main.py
│   ├── search_news.py
│   └── summarize_content.py
├── test/
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

### History

Search results from your topic search will be saved in the history subfolder. You can identify separate files by virtue of search term and date/time. 

### Design Choices Brainstorming

#### Flexibility with LangChain

LangChain was chosen to allow potential switching between different services, ensuring the project isn’t restricted to one service.

#### Community Focus with Hugging Face

Hugging Face was selected for its open-source nature and active community, providing access to state-of-the-art NLP models.

#### Transition to Pipelines

Initially, API endpoints were used, but issues with internal kwargs calls led to a transition to pipelines. This approach leverages local resources for more reliable processing.

#### TODO Modular API Calls

To improve maintainability, API calls are separated into utility functions, making the codebase cleaner and easier to manage.

#### TODO ANSI Colours 

To improve readability and usability, it would be nice to use ANSI Codes to make the terminal application pretty.

#### Verbose Main Script

The main script is currently verbose but maintains clarity and functionality. Future refactoring will focus on modularizing the code.

#### NER Limitations

Named Entity Recognition (NER) sometimes capitalizes normal words incorrectly. Although no workaround has been found yet, the pipeline’s keyword summarization remains effective.

