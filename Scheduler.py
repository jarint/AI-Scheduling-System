'''
This class is the container for the scheduling AI. It calls the methods in order to parse an input file and returns a completed
schedule at the end of the evaluation process.

'''

from ScheduleObjects.Schedule import Schedule
from Parser import Parser
from Search.Environment import Environment
from Search.SearchModel import SearchModel
from Search.Tree import Tree, Node


class Scheduler:
    stack = []
    current_best = None

    def __init__(self) -> None:
        self.tree = Tree()
        Scheduler.stack.append(self.tree.root)

    # start function internal methods start the search process
    def search(self):
        node = Scheduler.stack.pop()

        # Checking if we update current best
        if (node.sol == True):
            if not(Scheduler.current_best == None):
                if node.pr.penalty < Scheduler.current_best.pr.penalty:
                    Scheduler.current_best = node
                    print(self.current_best.pr.assignments)
            else:
                Scheduler.current_best = node
                print(self.current_best.pr.assignments)

        
        # Adding children to node
        self.tree.expand(node)
        node.check_sol()

        # Sorting children in reverse order
        if len(node.children) > 0:
            self.tree.fleaf(node)

        # Adding children in reverse order (so those with the lowest opt values are added most recently to the stack)
        for child in node.children:
            Scheduler.stack.append(child)

        if len(Scheduler.stack) != 0:
            return Scheduler.search()

        return Scheduler.current_best





