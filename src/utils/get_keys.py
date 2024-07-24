"""
get_keys.py

This module provides a function to load environment variables from a `.env` file
and retrieve their values. It uses the `python-dotenv` package to handle loading
variables from the file and `os` to access environment variables.

Functions:
    - get_env: Retrieves the value of an environment variable.

Usage Example:
    value = get_env("MY_ENV_VAR")
    print(value)
"""

# Import Relevant Packages
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

    Usage Example:
        value = get_env("MY_ENV_VAR")
        print(value)
    """

    load_dotenv()

    return os.getenv(key) if os.getenv(key) else os.environ.get(key)


if __name__ == "__main__":
    # Example usage
    env_var_name = "MY_ENV_VAR"  # Should be defined in .env file
    value = get_env(env_var_name)
    print(f"Value of '{env_var_name}': {value}")
