'''
This is the driver class. It creates a scheduler object and accepts

'''

import logging

from Search.Environment import Environment
from Scheduler import Scheduler
from Parser import Parser
from Printer import Printer

# sample input: python main.py sample_input.txt 2 3 4 5 6 7 8 9

class Main:

    @staticmethod
    def main():
        Main.clear_log()
        logging.basicConfig(filename="program_log.log", level=logging.DEBUG)

        Environment.pre_parser_initialization()
        parser = Parser()
        parser.parse()
        Environment.post_parser_initialization()
        Scheduler.initialize()

        for item in Environment.GAME_SLOT_ID_TO_OBJ.values():
            print(item.gamemax)
        
        optimal_solution = Scheduler.search()
        
        if optimal_solution == None:
            print("No solution was found!")
        else:
            #print("Solution: " + str(optimal_solution.pr.assignments))
            Printer.printSchedule(optimal_solution)
        # print("Eval-value: " + str(optimal_solution))
        # print(...)
    
    @staticmethod
    def clear_log():
        with open("program_log.log", "w"):
            pass

if __name__ == "__main__":
    Main.main()