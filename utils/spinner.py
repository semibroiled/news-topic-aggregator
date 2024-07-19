# Import Relevant Packages
import itertools
import threading
import time
import sys


class Spinner:
    def __init__(self, message="Loading", max_dots=3, load_speed=0.5):
        self.message = message
        self.load_speed = load_speed
        self.max_dots = max_dots
        self.dots = itertools.cycle(["." * i for i in range(self.max_dots + 1)])
        self.stop_running = False
        self.thread = threading.Thread(target=self.init_load_text)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_running = True
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + self.max_dots) + "\r")
        sys.stdout.flush()

    def init_load_text(self):
        while not self.stop_running:
            sys.stdout.write("\r" + self.message + next(self.dots))
            sys.stdout.flush()
            time.sleep(self.load_speed)


if __name__ == "__main__":
    spinner = Spinner("Something is loading dynamically")

    spinner.start()

    time.sleep(15)  # Simulate a process

    spinner.stop()
