'''
This class generates the and-tree, wherein each internal node will be a partially complete schedule and each 
leaf node will be a complete schedule. As such, every node in the tree will be a an object of the schedule class

'''

from ScheduleObjects.Schedule import Schedule
from Search.SearchModel import SearchModel
from Search.Environment import Environment


class Node:
    def __init__(self, parent, pr: Schedule, sol: bool):
        self.parent = parent
        self.pr = pr
        self.sol = sol
        self.children = []
        self.opt = None
        if self.parent != None:
            self.compute_opt()

    def check_sol(self):
        # if sol becomes yes, call parent.check_sol()
        pass

    def compute_opt(self):
        latest_id, latest_slot_id = self.pr.latest_assignment

        # We want to make assignments that fulfil hard constraints first, so we give those assignments infinitely negative values (else, we assign eval())
        if (latest_id in Environment.PARTASSIGN) and (latest_slot_id == Environment.PARTASSIGN[latest_id]):
            self.opt = float('-inf')
        elif (latest_id in Environment.SPECIAL_PRACTICE_BOOKINGS) and (latest_slot_id == Environment.SPECIAL_PRACTICE_BOOKINGS[latest_id]):
            self.opt = float('-inf')
        else:
            self.opt = self.eval()

    def eval(self):
        """
        Input: ...
        Output: ...
        Computes the penalty value of this node's schedule.
        """
        # TODO: code functionality for computing eval and return the value
        return 0

    def add_child(self, parent, pr, sol):
        self.children.append(Node(parent, pr, sol))


class Tree:
    current_stack = []

    # Empty constructor (TODO)
    def __init__(self) -> None:
        self.root = Node(None, Schedule(), False)
        Tree.current_stack.append(self.root)


    def erw(self, parent_node: Node):
        for schedule in SearchModel.div(parent_node.pr):
            parent_node.add_child(parent_node, schedule, False)


    def fleaf(self, parent_node: Node):
        if not(len(parent_node.children) > 0):
            raise(RuntimeError("fleaf attempting to choose child from parent with no children"))

        # Sorting children by Opt values
        parent_node.children.sort(key=lambda x: x.opt)

        # Choosing leftmost child
        return parent_node.children[0]