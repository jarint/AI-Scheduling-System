'''
The methods inside this classs will check that a generated schedule passes the Hard constraints of the problem.
If the schedule does not pass hard constraints, it will deleted, never having been placed into our tree.

'''

# Constraint checks will take as input a current schedule and a new game or practice slot assignment to make.

from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.Slot import Slot


class HardConstraint:
    @staticmethod
    def check_constraints():
        # if (game): check_game_constraints()
        # else: check_practice_constraints
        # check_city_constraints
        pass

    class GeneralConstraints:
        @staticmethod
        def check_game_constraints(schedule: Schedule, game: Game, slot: Slot):
            pass

        @staticmethod
        def check_practice_constraints(schedule: Schedule, practice: Practice, slot: Slot):
            pass
        
        @staticmethod
        def game_max():
            pass

        @staticmethod
        def practice_max():
            pass

        # Game/practice same slot assignment
        @staticmethod
        def gp_same_slot():
            pass
        
        # Not compatible assignment
        @staticmethod
        def not_compatible():
            pass

        # Partial assignment
        @staticmethod
        def part_assign():
            pass

        # Unwanted assignment
        @staticmethod
        def unwanted():
            pass

    class CityConstraints:
        def check_city_constraints():
            pass