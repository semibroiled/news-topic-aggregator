#!/bin/bash

# Function to run application locally
run_app() {
    # Activate Virtual Environment
    source .venv/bin/activate
    # Export Python Path to include src
    export PYTHONPATH=$PYTHONPATH:./src
    # Download SpaCy Packs if choosing SpaCy over NLTK
    # python -m spacy download en_core_web_lg
    # python -m spacy download de_core_news_lg
    # Run CLI app
    python main.py
    # Deactivate Venv
    deactivate
}

run_app_with_test(){
    # Activate Virtual Environment
    source .venv/bin/activate
    # Export Python Path to include src
    export PYTHONPATH=$PYTHONPATH:./src
    # Download SpaCy Packs if choosing SpaCy over NLTK
    # python -m spacy download en_core_web_lg
    # python -m spacy download de_core_news_lg
    # Run Pytest suite
    pytest
    # Run CLI app
    python main.py
    # Deactivate Venv
    deactivate
}

run_docker(){
    # Build Docker Image
    echo "Building Docker Image..."
    docker build -t news-topic-aggregator .

    # Run Container with .env file and volume mount
    echo "Running Docker..." 
    echo "Make sure .env and /history is configured correctly"
    docker run -it --rm --env-file .env -v "$(pwd)/history:/app/history" news-topic-aggregator
}

# Check flags to decide what to run
# Check the provided flag
if [ "$1" == "--run" ]; then
    run_app
elif [ "$1" == "--test" ]; then
    run_app_with_test
elif [ "$1" == "--docker" ]; then
    run_docker
else
    echo "Invalid option. Use --run to run the application locally; \ 
    and --run-test for pytest execution before startin application; \
    or --docker to run with Docker."
fi