"""
This module provides a Spinner class to display a spinning animation in the console
while a running process is executing. The spinner runs in a separate thread and
can be customized with different messages and animation speeds.
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
            message (str, optional): Message to display. Defaults to "Loading...".
            animation_speed (float, optional): Speed of spinner animation in seconds. Defaults to 0.1.
        """
        self.message = message
        self.animation_speed = animation_speed
        self.spinner: Iterator[str] = itertools.cycle(["/", "─", "\\", "|"])
        self.stop_running: bool = False
        self.thread: threading.Thread = threading.Thread(target=self._spin)

    def start(self) -> None:
        """Start new thread for spinner animation"""
        self.stop_running = False
        self.thread.start()

    def stop(self) -> None:
        """Stop spinner animation and clear out line"""
        self.stop_running = True
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 1) + "\r")
        sys.stdout.flush()

    def _spin(self) -> None:
        """Update spinner animation until stop is called"""
        while not self.stop_running:
            sys.stdout.write("\r" + self.message + next(self.spinner))
            sys.stdout.flush()
            time.sleep(self.animation_speed)


if __name__ == "__main__":
    # Usage Example
    spinner = Spinner("Something is loading dynamically...")

    spinner.start()

    time.sleep(15)  # Simulate a process

    spinner.stop()
