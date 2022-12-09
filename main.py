'''
This is the driver class. It creates a scheduler object and accepts

'''

import logging
import time
import threading

from Search.Environment import Environment
from Scheduler import Scheduler
from Parser import Parser
from Printer import Printer
from Constraints.HardConstraints import HardConstraints

# sample input: python main.py sample_input.txt 2 3 4 5 6 7 8 9

class Main:
    search_complete = False

    @staticmethod
    def main():
        Main.clear_log()
        logging.basicConfig(filename="program_log.log", level=logging.DEBUG)

        Environment.pre_parser_initialization()
        parser = Parser()
        parser.parse()
        Environment.post_parser_initialization()
        Scheduler.initialize()

        # for item in Environment.GAME_SLOT_ID_TO_OBJ.values():
        #     print(item.gamemax)

        threading.Thread(target=Main.display_current_opt).start()
        
        optimal_solution = Scheduler.search()
        Main.search_complete = True
        
        if optimal_solution == None:
            print("No solution was found!")
        else:
            #print("Solution: " + str(optimal_solution.pr.assignments))
            Printer.print_schedule(optimal_solution.pr)
        # print("Eval-value: " + str(optimal_solution))
        # print(...)
    
    @staticmethod
    def clear_log():
        with open("program_log.log", "w"):
            pass
    
    @staticmethod
    def display_current_opt():
        while not Main.search_complete:
            time.sleep(4)
            if Scheduler.current_best != None:
                Printer.print_schedule(Scheduler.current_best.pr)
            else:
                print("\nNo solution yet among " + str(Environment.leaves_encountered) + " leaves encountered. Keep waiting!\n")
            total_fails = HardConstraints.general_fails + HardConstraints.city_fails
            print("\nGeneral fails: " + str(round(HardConstraints.general_fails / total_fails, 3)))
            print("     Game max fails: " + str(round(HardConstraints.game_max_fails / HardConstraints.general_fails, 3)))
            print("     Practice max fails: " + str(round(HardConstraints.practice_max_fails / HardConstraints.general_fails, 3)))
            print("     Same slot fails: " + str(round(HardConstraints.same_slot_fails / HardConstraints.general_fails, 3)))
            print("     Not compatible fails: " + str(round(HardConstraints.not_compatible_fails / HardConstraints.general_fails, 3)))
            print("     Part assign fails: " + str(round(HardConstraints.part_assign_fails / HardConstraints.general_fails, 3)))
            print("     Unwanted fails: " + str(round(HardConstraints.unwanted_fails / HardConstraints.general_fails, 3)))
            print("\nCity fails: " + str(round(HardConstraints.city_fails / total_fails, 3)) + "\n")

if __name__ == "__main__":
    Main.main()