"""
spinner.py

This module provides a Spinner class to display a spinning animation in the console
while a running process is executing. The spinner runs in a separate thread and
can be customized with different messages and animation speeds.

Classes:
    - Spinner: A class to create and manage a spinner animation in the console.

Usage Example:
    spinner = Spinner("Loading...")
    spinner.start()
    # Simulate a process
    time.sleep(5)
    spinner.stop()

    # With Context Manager
    with Spinner("Loading in context..."):
        time.sleep(5)
"""

# Import Relevant Packages
import itertools
import threading
import time
import sys

# Type Hints
from typing import Iterator


class Spinner:
    def __init__(
        self, message: str = "Loading...", animation_speed: float = 0.1
    ) -> None:
        """
        Initialize spinner with display message and animation speed

        Args:
            message (str): Message to display. Defaults to "Loading...".
            animation_speed (float): Speed of spinner animation in seconds. Defaults to 0.1.
        """
        self.message = message
        self.animation_speed = animation_speed
        self.spinner_sequence: Iterator[str] = itertools.cycle(["/", "─", "\\", "|"])
        self.stop_spinner: bool = False
        self.thread: threading.Thread = threading.Thread(target=self._spin)

    def __enter__(self) -> "Spinner":
        """Start Spinner animation when entering context"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Stop spinner animation when exiting context.
        Clean out resources.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception instance.
            traceback (traceback): The traceback object.
        """
        self.stop()

    def start(self) -> None:
        """Start new thread for spinner animation"""
        if not self.thread.is_alive():
            self.stop_spinner = False
            self.thread.start()

    def stop(self) -> None:
        """Stop spinner animation and clear out line"""
        self.stop_spinner = True
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

    def _spin(self) -> None:
        """Update spinner animation until stop is called"""
        while not self.stop_spinner:
            sys.stdout.write("\r" + self.message + next(self.spinner_sequence))
            sys.stdout.flush()
            time.sleep(self.animation_speed)


if __name__ == "__main__":
    # Usage Example
    print("Using Spinner normally")
    spinner = Spinner("Something is loading dynamically...")

    spinner.start()

    time.sleep(10)  # Simulate a process

    spinner.stop()

    # With Context Manager
    print("Using Spinner in context manager")
    with Spinner("Something is loading dynamically in a context..."):
        time.sleep(10)  # Simulate a process
