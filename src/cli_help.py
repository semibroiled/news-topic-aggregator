"""
cli_help.py

This module provides a function to output a help message for a Command Line Interface (CLI) application.
The help message includes instructions for language settings, application settings, and advanced query options.

Functions:
    - help_command_output: Returns a formatted help message string for the CLI application.

Usage Example:
    help_text = help_command_output()
    print(help_text)
"""


def help_command_output() -> str:
    """
    Returns a formatted help message string for the CLI application.

    The help message includes information on:
    - Language settings and how to change the query language.
    - Application settings and how to exit the application.
    - Advanced queries with examples of exact match and Boolean operators.

    Returns:
        str: The formatted help message string.

    Usage:
        help_text = help_command_output()
        print(help_text)
    """
    return """
- Language Settings\n\
    \t-- Use command '!setlang' on prompt to change query language\n\
    \t-- Type 'en' for English and 'de' for German\n\
- Application Settings\n\
    \t-- Type in '!exit' or '!quit' to close application\n\
- Summarization Settings\n\
    \t-- Type in '!sethf' to set Model IDs for HuggingFace\n\
- Advanced Queries\n\
    \t--Put your topic in quotation marks for exact match. (eg: \"elon musk\")\n\
    \t--Use Boolean Operators. (eg: (crypto AND bitcoin) NOT ethereum)"""


# Example usage
if __name__ == "__main__":
    help_text = help_command_output()
    print(help_text)
