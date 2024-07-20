"""
Module for retrieving environment variables.

This module provides a function to load environment variables from a `.env` file
and retrieve their values. It uses the `python-dotenv` package to handle loading
variables from the file and `os` to access environment variables.

Functions:
    get_env(key: str) -> Optional[str]: Retrieves the value of an environment variable.
"""

import os
from dotenv import load_dotenv

# Type Hints
from typing import Optional


# Function to get Envrionment Variables
def get_env(key: str) -> Optional[str]:
    """
    Retrieve the value of an environment variable.

    This function first loads environment variables from a `.env` file, if it exists.
    Then, it tries to retrieve the value of the specified environment variable from the
    environment. If the variable is not found, it returns None.

    Args:
        key (str): The name of the environment variable to retrieve.

    Returns:
        Optional[str]: The value of the environment variable, or None if not found.
    """

    load_dotenv()

    return os.getenv(key) if os.getenv(key) else os.environ.get(key)
