'''
This class is the container for the scheduling AI. It calls the methods in order to parse an input file and returns a completed
schedule at the end of the evaluation process.

'''

from ScheduleObjects.Schedule import Schedule
from Parser import Parser
from Search.Environment import Environment
from Search.SearchModel import SearchModel
from Search.Tree import Tree, Node
from Printer import Printer


class Scheduler:
    tree = None
    stack = []
    current_best = None

    @staticmethod
    def initialize():
        Scheduler.tree = Tree()
        Scheduler.stack.append(Scheduler.tree.root)


    # start function internal methods start the search process
    @staticmethod
    def search():
        print("Search has started.")
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

        return Scheduler.current_best