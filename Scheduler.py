'''
This class is the container for the scheduling AI. It calls the methods in order to parse an input file and returns a completed
schedule at the end of the evaluation process.

'''

import time

from ScheduleObjects.Schedule import Schedule
from Constraints.HardConstraints import HardConstraints
from Parser import Parser
from Search.Environment import Environment
from Search.SearchModel import SearchModel
from Search.Tree import Tree, Node
from Printer import Printer


class Scheduler:
    tree = None
    stack = []
    current_best = None
    last_print_time = time.time()


    @staticmethod
    def initialize():
        Scheduler.tree = Tree()
        Scheduler.stack.append(Scheduler.tree.root)


    # start function internal methods start the search process
    @staticmethod
    def search():
        print("Search has started.")

        solvable = Scheduler.detect_solvable()
        if not solvable:
            print("Instance doesn't appear to be solvable!")
            return None

        while len(Scheduler.stack) > 0:
            # print("Stack size: " + str(len(Scheduler.stack)))
            node: Node = Scheduler.stack.pop()

            total_activities = len(Environment.ACTIVITY_IDS)
            remaining_activities = len(node.pr.remaining_games) + len(node.pr.remaining_practices)
            # print(total_activities - remaining_activities)
            
            # Adding children to node
            Scheduler.tree.expand(node)
            node.check_sol()

            # Checking if we update current best
            if (node.sol == True):
                if not(Scheduler.current_best == None):
                    if node.pr.eval < Scheduler.current_best.pr.eval:
                        Scheduler.current_best = node
                        # print(Scheduler.current_best.pr.assignments)
                else:
                    Scheduler.current_best = node
                    # print(Scheduler.current_best.pr.assignments)

            # Sorting children in reverse order
            if len(node.children) > 0:
                # print("Node has children")
                Scheduler.tree.fleaf(node)
            else:
                # print("Node does not have children")
                pass

            # Adding children in reverse order (so those with the lowest opt values are added most recently to the stack)
            for child in node.children:
                Scheduler.stack.append(child)

            Scheduler.display_current_opt()

        return Scheduler.current_best

    
    @staticmethod
    def display_current_opt():
        if time.time() - Scheduler.last_print_time > 4:
            Scheduler.last_print_time = time.time()
            total_fails = HardConstraints.general_fails + HardConstraints.city_fails
            print("\nGeneral fails: " + str(round(HardConstraints.general_fails / total_fails, 3)))
            print("     Game max fails: " + str(round(HardConstraints.game_max_fails / HardConstraints.general_fails, 3)))
            print("     Practice max fails: " + str(round(HardConstraints.practice_max_fails / HardConstraints.general_fails, 3)))
            print("     Same slot fails: " + str(round(HardConstraints.same_slot_fails / HardConstraints.general_fails, 3)))
            print("     Not compatible fails: " + str(round(HardConstraints.not_compatible_fails / HardConstraints.general_fails, 3)))
            print("     Part assign fails: " + str(round(HardConstraints.part_assign_fails / HardConstraints.general_fails, 3)))
            print("     Unwanted fails: " + str(round(HardConstraints.unwanted_fails / HardConstraints.general_fails, 3)))
            print("\nCity fails: " + str(round(HardConstraints.city_fails / total_fails, 3)) + "\n")
            if Scheduler.current_best != None:
                Printer.print_schedule(Scheduler.current_best.pr)
            else:
                print("\nNo solution yet among " + str(Environment.leaves_encountered) + " leaves encountered. Keep waiting!\n")

        
    @staticmethod
    def detect_solvable():
        total_gamemax = sum(list(map(lambda x: x.gamemax, Environment.GAME_SLOT_ID_TO_OBJ.values())))
        total_practicemax = sum(list(map(lambda x: x.practicemax, Environment.PRACTICE_SLOT_ID_TO_OBJ.values())))
        num_games = len(Environment.GAME_IDS)
        num_practices = len(Environment.PRACTICE_IDS)

        if num_practices > total_practicemax:
            False
        
        if num_games > total_gamemax + 2: # + 2 for the special game bookings which are placed in practice slots
            return False

        return True