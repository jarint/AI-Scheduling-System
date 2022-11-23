'''
This class generates the and-tree, wherein each internal node will be a partially complete schedule and each 
leaf node will be a complete schedule. As such, every node in the tree will be a an object of the schedule class

'''

from ScheduleObjects.Schedule import Schedule

class Tree:

    # Empty constructor (TODO)
    def __init__(self) -> None:
        self.root = self.Node(None, Schedule(), False)

    class Node:
        def __init__(self, parent, pr: Schedule, sol: bool):
            self.parent = parent
            self.pr = pr
            self.sol = sol
            self.children = []

        def produce_children(self, schedules):
            # div
            pass

        def check_sol(self):
            # if sol becomes yes, call parent.check_sol()
            pass