'''
The methods inside this classs will check that a generated schedule passes the Hard constraints of the problem.
If the schedule does not pass hard constraints, it will deleted, never having been placed into our tree.

'''

# Constraint checks will take as input a current schedule and a new game or practice slot assignment to make.

from ScheduleObjects.Activity import Activity
from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.ActivitySlot import ActivitySlot


class HardConstraints:
    @staticmethod
    def check_constraints(schedule: Schedule, activity: Activity, slot: ActivitySlot):
        passes = True
        if (isinstance(activity, Game)):
            passes = passes and HardConstraints.GeneralConstraints.check_game_constraints()
        elif (isinstance(activity, Practice)):
            passes = passes and HardConstraints.GeneralConstraints.check_practice_constraints()
        else:
            raise TypeError("Activity given to 'check_constraints method must be either of type 'Game' or type 'Practice'")
        passes = passes and HardConstraints.CityConstraints.check_city_constraints()
        return passes

    class GeneralConstraints:
        @staticmethod
        def check_game_constraints(schedule: Schedule, game: Game, slot: ActivitySlot):
            pass

        @staticmethod
        def check_practice_constraints(schedule: Schedule, practice: Practice, slot: ActivitySlot):
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
        def not_compatible(id: str, slot: list):
            # id is the id of the activity being added and slot is the list of activity ids for the slot that id is being added to
            for act in slot:
                if id == act: return False

        # Partial assignment
        @staticmethod
        def part_assign():
            pass

        # Unwanted assignment
        @staticmethod
        def unwanted():
            pass

    class CityConstraints:
        @staticmethod
        def check_city_constraints():
            pass

        @staticmethod
        def evening_slot_constraint():
            pass

        @staticmethod
        def age_group_constraint():
            pass
        
        @staticmethod
        def meeting_constraint():
            pass
        
        @staticmethod
        def special_game_constraint():
            pass