'''
This is the driver class. It creates a scheduler object and accepts

'''

import logging

from Search.Environment import Environment
from Scheduler import Scheduler

# sample input: python main.py sample_input.txt 2 3 4 5 6 7 8 9

class Main:

    @staticmethod
    def main():
        Main.clear_log()
        logging.basicConfig(filename='program_log.log', encoding='utf-8', level=logging.DEBUG)
        s = Scheduler()
        s.search()
    
    
    @staticmethod
    def clear_log():
        with open("program_log.log", "w"):
            pass

if __name__ == "__main__":
    Main.main()