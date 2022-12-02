'''
This is the driver class. It creates a scheduler object and accepts

'''

import logging

from Scheduler import Scheduler

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