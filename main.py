import os
import csv
import pandas as pd

import itertools
import threading
import time
import sys

from enum import Enum

class ApplicationMode(Enum):
    RUN_CONTINUOUSLY = True



def main():
    print("Starting Application...")
    
    while ApplicationMode.RUN_CONTINUOUSLY.value:
        topic = input(
            "What topic would you like to search? Enter 'exit' or 'quit' to close application\n"
        )
        if topic.strip().lower() == "exit" or "quit":
            break

        print(f"Alright! Searching the web for articles about '{topic}'")




if __name__ == "__main__":
    main()
