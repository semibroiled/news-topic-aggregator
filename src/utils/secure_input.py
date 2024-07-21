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
    # Basic sanitizatio
    # Basic sanitization to remove potentially harmful characters
    sanitized_input = re.sub(r"[^a-zA-Z0-9\s!\"]", "", user_input)
    return sanitized_input


if __name__ == "__main__":
    # Example input
    input_string = "import os.rmdir"
    sanitized_string = sanitize_input(input_string)

    print(f"Original Input: {input_string}")
    print(f"Sanitized Input: {sanitized_string}")