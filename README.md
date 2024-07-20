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
=> `pytest`
or =>`pytest -v` for detailed output in verbose mode
=> `pytest -s` to show print statements
=> `pytest -x` to stop after first FAIL

Run pytest for a specific file
=> `pytest path/to/test_file.py`

Run specific test within a file
=> `pytest path/to/test_file.py::test_case_name`

## Configuring .env

Rename the `.env.example` file to `.env`

Enter your API Key for News API instead of the example listed.

## Setting up News API Token

1. Make an account at https://newsapi.org/
2. Press *Get API Key->* Button on Homepage
3. You will be offered a free development API Key. Be sure to save it and use it

## Navigating the Application

Upon running the application, you will be prompted to enter a topic to search. You can also use the following commands:

-> !help - Display usage instructions.
-> !setlang - Change query language.
-> !exit or !quit - Close the application.

## Project Structure

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

### History

Search results from your topic search will be saved in the history subfolder. You can identify separate files by virtue of search term and date/time. 