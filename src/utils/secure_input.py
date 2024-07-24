"""
secure_input.py

This module provides a function to sanitize user input by removing potentially harmful characters.
The function removes any characters from the input string that are not alphanumeric, whitespace, 
or specific allowed punctuation. This helps to prevent code injection or other security vulnerabilities.

Functions:
    - sanitize_input: Removes potentially harmful characters from a user input string.
    - sanitize_model_name: Removes potentially harmful characters from a user input string for model ID.


Usage Example:
    sanitized_string = sanitize_input("import os.rmdir")
    print(sanitized_string)  # Output: import osrmdir
"""

# Import Relevant Packages
import re


def sanitize_input(user_input: str) -> str:
    """
    Sanitize the user input by removing potentially harmful characters.

    This function removes any characters from the input string that are not
    alphanumeric or whitespace. This helps to prevent code injection or other
    security vulnerabilities.

    Args:
        user_input (str): The input string to be sanitized.

    Returns:
        str: The sanitized input string.
    """
    # Basic sanitization to remove potentially harmful characters
    sanitized_input = re.sub(r"[^a-zA-Z0-9\s!\"]", "", user_input)
    return sanitized_input


def sanitize_model_name(model_name: str) -> str:
    """
    Sanitize the user input of model by removing potentially harmful characters.

    This function removes any characters from the input string that are not
    alphanumeric or whitespace. This helps to prevent code injection or other
    security vulnerabilities.

    Args:
        model_name (str): The input model name string to be sanitized.

    Returns:
        str: The sanitized input model name string.
    """
    # Basic sanitization to remove potentially harmful characters
    sanitized_input = re.sub(r"[^a-zA-Z0-9-/]", "", model_name)
    return sanitized_input


if __name__ == "__main__":
    # Example input
    input_string = "import os.rmdir"
    sanitized_string = sanitize_input(input_string)

    print(f"Original Input: {input_string}")
    print(f"Sanitized Input: {sanitized_string}")
