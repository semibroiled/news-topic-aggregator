#!/bin/bash

# Function to run application locally
run_app() {
    # Activate Virtual Environment
    source .venv/bin/activate
    # Export Python Path to include src
    export PYTHONPATH=$PYTHONPATH:./src
    # Run CLI app
    python src/main.py
    # Deactivate Venv
    deactivate
}

run_app_with_test(){
    # Activate Virtual Environment
    source .venv/bin/activate
    # Export Python Path to include src
    export PYTHONPATH=$PYTHONPATH:./src
    # Run Pytest suite
    pytest
    # Run CLI app
    python src/main.py
    # Deactivate Venv
    deactivate
}

run_docker(){
    # Build Docker Image
    docker build -t news-topic-aggregator .

    # Run Container with .env file
    docker run -it --rm --env-file .env news-topic-aggregator
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