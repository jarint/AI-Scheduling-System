'''
The methods inside this classs will check that a generated schedule passes the Hard constraints of the problem.
If the schedule does not pass hard constraints, it will deleted, never having been placed into our tree.

'''

# Constraint checks will take as input a current schedule and a new game or practice slot assignment to make.

from Enumerations import ActivityType, Weekday
from Search.Environment import Environment
from ScheduleObjects.Activity import Activity
from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.ActivitySlot import ActivitySlot
from Enumerations import ActivityType
from Parser import Parser


class HardConstraints:

    @staticmethod
    def check_constraints(schedule: Schedule, assignment): # TODO: add type of 'assignment' parameter
        # Index 1 of latest_assignment is the slot ID, so index 0 of that is the activity type
        activity_type = assignment[1][0]

        passes = True
        if (activity_type == ActivityType.GAME):
            passes = passes and HardConstraints.GeneralConstraints.check_game_constraints(schedule, assignment)
        elif (activity_type == ActivityType.PRACTICE):
            passes = passes and HardConstraints.GeneralConstraints.check_practice_constraints(schedule, assignment)
        else:
            raise TypeError("Invalid activity type of latest assignment in 'check_activity_constraints()' method")
        return passes and HardConstraints.CityConstraints.check_city_constraints(schedule, assignment)


    # TODO: update all constraint check methods to use 'assignment' as second parameter instead of 'schedule.latest_assignment'
        # note that assignment[0] is an activity ID (str) and assignment[1] is a slot ID (tuple)
            # slot_id[0] is an activity type (ActivityType), slot_id[1] is a weekday (Weekday), and slot_id[2] is a start time (str)
                # the ActivityType and WeekDay classes can be found in Enumerations.py


    class GeneralConstraints:
        @staticmethod
        def check_game_constraints(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass


        @staticmethod
        def check_practice_constraints(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass


        @staticmethod
        def game_max(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass


        @staticmethod
        def practice_max(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass


        # Game/practice same slot assignment
        @staticmethod
        def gp_same_slot(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass
        

        # Not compatible assignment
        @staticmethod
        def not_compatible(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            for id in schedule.assignments[slot_id]:
                if Environment.NOT_COMPATIBLE[activity_id].contains(id): 
                    return False
            return True


        # Partial assignment
        @staticmethod
        def part_assign(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = schedule.latest_assignment
            for id in schedule.assignments[slot_id]:
                if Environment.NOT_COMPATIBLE[activity_id].contains(id): 
                    return True
            return False


        # Unwanted assignment
        @staticmethod
        def unwanted(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            for slot in Environment.UNWANTED[activity_id]:
                if slot_id == slot:
                    return False
            
            return True


    class CityConstraints:
        
        @staticmethod
        def check_city_constraints(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass


        @staticmethod
        def evening_slot_constraint(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            pass


        @staticmethod
        def age_group_constraint(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            

        # May be better to include the Tuesday meeting slot, but assign it a game min/max of 0
        @staticmethod
        def meeting_constraint(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            activity_type, weekday, start_time = slot_id
            if (weekday == Weekday.TU 
                and start_time in ["11:00", "12:00"] 
                and len(schedule.assignments[slot_id]) > 0
            ):
                return False
            else:
                return True
        

        @staticmethod
        def special_bookings_constraint(schedule: Schedule, latest_assignment: tuple) -> bool:
            activity_id, slot_id = latest_assignment
            if activity_id not in Environment.SPECIAL_PRACTICE_BOOKINGS:
                return True
            
            if slot_id == (ActivityType.PRACTICE, Weekday.TU, "18:00-19:00"):
                return True
            else:
                return False