# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy NLP Models
# RUN python -m spacy download en_core_web_lg
# RUN python -m spacy download de_core_news_lg

# Copy the rest of the application's code into the container at /app
COPY . /app

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app


# Run the main.py when the container launches
CMD ["python", "main.py"]