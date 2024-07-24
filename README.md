# News Topic Aggregator

This project is a CLI Apllication that searches for recent news articles on a given topic and generates a summary of the top articles

## Installation

Note: Unless stated specifically, most commands are UNIX specific. Windows Devices using powershell have a different suite of commands.

1. Clone the repository: 
   => ```git clone link-to-repository```
2. Enter cloned directory
    => `cd news-topic-aggregator`

3. Create Virtual Environment
    => Make sure you have Python installed. Python 3.12 is reccomennded
    => `python3 -m venv .venv`

4. Activate the Virtual Environment
    => `source .venv/bin/activate`
    => on Windows Devices, this is `.venv\Scripts\activate`

5. Verify you are in the correct envrironment
    => `which pip` and `which python` to check if you're in .venv

6. Install required packages
    => `pip install -r requirements.txt`

### Configuring .env

Rename the `.env.example` file to `.env`

Enter your API Key for News API instead of the example listed.

See below on how to obtain your API Key

### Setting up News API Token

1. Make an account at https://newsapi.org/
2. Press **Get API Key->** Button on Homepage
3. You will be offered a free development API Key. Be sure to save it and use it

## Usage

There are a couple different ways to start the application.

 
### 1. Running from the terminal
Run the application in your terminal. Make sure you're already in the project's root directory

`python main.py`

If you're getting Import Errors such as no module named 'src'; update PYTHONPATH and then run `main.py`

```sh
export PYTHONPATH="${PYTHONPATH}:/path/to/project_root/src"
python main.py
```

### 1.1. Run Unit Tests

To run tests, from the project directory in terminal use command:
1. => `pytest`
2. or =>`pytest -v` for detailed output in verbose mode
3. => `pytest -s` to show print statements
4. => `pytest -x` to stop after first FAIL

5. Run pytest for a specific file
 => `pytest path/to/test_file.py`

6. Run specific test within a file
=> `pytest path/to/test_file.py::test_case_name`

### 2. Running in Docker

To Run in Docker, you need to have Docker Desktop installed and running in the background. From your repository, use

1. `docker build -t news-topic-aggregator .`
2. `docker run -it --rm --env-file .env -v "$(pwd)/history:/app/history" news-topic-aggregator`

 - With the `--env-file flag` we specify our `.env` file from which the API Key is read
 - With `-v` flag we set the output where the CSV files are written locally
 - With the `it` flag we run interactively on the terminal and accept user inputs, this means that you can run `pytest` in the Terminal via Docker
  
#### 2.1. Setting Docker Settings

On macOS and Windows

Docker Desktop provides a graphical interface to allocate more resources to Docker.

1.	Open Docker Desktop:
	•	Click on the Docker icon in the taskbar to open Docker Desktop.
2.	Go to Settings/Preferences:
	•	Click on the Settings or Preferences menu item. This is usually found in the Docker Desktop menu.
3.	Adjust Resources:
	•	Navigate to the Resources section (on the left sidebar).
	•	You can adjust the sliders for:
	•	CPU: Increase the number of CPUs allocated.
	•	Memory: Increase the amount of RAM allocated.
	•	Swap: Adjust the swap space if needed.
	•	Disk: Increase disk space allocation if needed.
4.	Apply and Restart:
	•	After making adjustments, click Apply & Restart to apply the new settings and restart Docker.

Do this if your container keeps crashing after the first query. 

Due to running HuggingFace locally, this may generate too much resources for a container to run without restrictions leading it to eventually crash.

### 3. Shell Script to Run it with PYTHONPATH exported

This is a simple Shell script to run the application on UNIX devices in **bash**. You do need to make sure that the `.env` file with API Key and `.venv` is already correctly configued. This streamlines all the nitty gritty steps and reduces inconvenience.

You do not need to activate the virtual envrionment, as that is a specified step in the script itself.


1. `chmod +x start.sh` to set the file as an executable
2. `./start.sh --run` or `./start.sh --test` or `./start.sh --docker`

- `--run` flag starts the application
- `--test` flag runs pytest suite before starting application
- `--docker` flag builds docker image and runs container


## Navigating the CLI Application

Upon running the application, you will be prompted to enter a topic to search. You can also use the following commands:

- !help - Display usage instructions.
- !setlang - Change query language.
- !sethf - Change Model ID for HuggingFace.
- !exit or !quit - Close the application.
 
### Language Settings

To change the query language, use the !setlang command. Type en for English or de for German.

Application Defaults to English.

### HuggingFace Model Settings

To change the model used for summarization, use !sethf command.

Application Defaults to Barts CNN Model.

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
│
├── src/
│   ├── utils/
│   │   ├── secure_input.py
│   │   ├── get_keys.py
│   │   ├── spinner.py
│   │   └── __init__.py
│   ├── cli_help.py
│   ├── search_news.py
│   └── summarize_content.py
├── test/
├── main.py
├── .env
├── .env.example
├── config.yaml
├── LICENSE
├── start.sh
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

Hugging Face was selected for its open-source nature and active community, providing access to state-of-the-art NLP models. Especially for our case, we use Bart trained on CNN News Articles.

Despite that, the performance is anything but optimal. Often only part of headlines verbatim or misconstrued repeatable inferences are outputted instead.

Update: Added option to type in other models.

#### Transition to Local Pipelines

Initially, API endpoints were used, but issues with internal kwargs calls led to a transition to pipelines. This approach leverages local resources for more reliable processing in terms of execution.

In terms of results, it seems to just fetch one or two headlines in full. At present, I do not know a optimzation strategy suited for this issue.

#### TODO Modular API Calls

To improve maintainability, API calls are separated into utility functions, making the codebase cleaner and easier to manage.

Update: I've decided against this to reduce overhead.

#### TODO ANSI Colours 

To improve readability and usability, it would be nice to use ANSI Codes to make the terminal application pretty.

#### Verbose Main Script

The main script is currently verbose but maintains clarity and functionality. Future refactoring will focus on modularizing the code. Especially using a terminal package instead of input and to handle all steps within try-except blocks where necessary.

#### NER Limitations

Named Entity Recognition (NER) sometimes captures capitalization of normal words incorrectly. No work around has been found. Packages NLTK and SpaCy were both tested. Despite NLTKs false positives, it was chosen in favour of SpaCy due to it not capturing obvious NEs in testing phase. 

This is a known limitation and its optimization is beyond my knowlegdge for now.

#### Date From and To Handling

I took the 'at least one month' and took the liberty to interpret it as 
for the last month only for the sake of convenienve. Despite plenty of neat stuff there is no way to set that within CLI

Update: I see no reason to limit to one month in hindsight, removing date constraint so it fetches all the data it can

#### CLI is done with Input and Print

I didn't use argparse or really my favourites click/questionary to make the CLI. That was a hindsight. I am too used the past month to make CLIs in C++ and zoned myself in. It works, so I don't plant to fix that soon. Neat todo for later

#### Application is slow

The application is a bit bloated perhaps and hence slow. The first few dozen runs it wasn't really like that. It just sort of happened. 

I suspect exporting PYTHONPATH temporarily so many times might have done something, or just that the runtime itself is slow due to many unoptimized elements. 

Not to mention, I am running HF locally instead of calling via API. As I was coding trying to march past depreceated commands, I eventually ran into a problem where internal method calls I have no control over are hindering code execution. This is beyond the scope of this project, and thus I have decided to run it locally instead.

Another issue of contention is nltk or spacy. Since they are downloaded on memory, they may also be causing performance issues.

#### Sanitized Inputs

I wanted to let '!' still be the basis for my CLI Commands so I let it pass through sanitization process of inputs- there should be a better or more robust way to do this. 

#### Match statement for HTTP Errors

Its verbose and unnecessary, I had it in when I was coding and debugging, and kept it inside still. It would be a good idea to take them out for clarity in code. 

Update: Removed from code

