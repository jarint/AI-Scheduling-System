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
from Parser import Parser


class HardConstraints:

    @staticmethod
    def check_constraints(schedule: Schedule, activity: Activity, slot: ActivitySlot):
        passes = True
        if (activity.ACTIVITY_TYPE == ActivityType.GAME):
            passes = passes and HardConstraints.GeneralConstraints.check_game_constraints()
        elif (activity.ACTIVITY_TYPE == ActivityType.PRACTICE):
            passes = passes and HardConstraints.GeneralConstraints.check_practice_constraints()
        else:
            raise TypeError("Activity given to 'check_constraints method must be either of type 'Game' or type 'Practice'")
        return passes and HardConstraints.CityConstraints.check_city_constraints()


    class GeneralConstraints:

        @staticmethod
        def check_game_constraints(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass


        @staticmethod
        def check_practice_constraints(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass


        @staticmethod
        def game_max(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass


        @staticmethod
        def practice_max(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass


        # Game/practice same slot assignment
        @staticmethod
        def gp_same_slot(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass
        

        # Not compatible assignment
        @staticmethod
        def not_compatible(schedule: Schedule, latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]") -> bool:
            latest_id, latest_slot = latest_assignment
            for id in schedule.assignments[latest_slot]:
                # if env.NOT_COMPATIBLE[latest_id].contains(id): return False
                pass
            
            return True


        # Partial assignment
        @staticmethod
        def part_assign(schedule: Schedule, latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]") -> bool:
            latest_id, latest_slot = latest_assignment
            for id in schedule.assignments[latest_slot]:
                # if env.NOT_COMPATIBLE[latest_id].contains(id): return True
                pass
            
            return False


        # Unwanted assignment
        @staticmethod
        def unwanted(schedule: Schedule, latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]") -> bool:
            latest_id, latest_slot = latest_assignment
            # for slot in env.UNWANTED[latest_id]:
            #     if latest_slot == slot:
            #         return False
            return True


    class CityConstraints:

        SPECIAL_PRACTICE_BOOKINGS = {
            "CMSA U12T1S": (ActivityType.PRACTICE, Weekday.TU, "18:00"), 
            "CMSA U13T1S": (ActivityType.PRACTICE, Weekday.TU, "18:00")
        }

        @staticmethod
        def check_city_constraints(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass


        @staticmethod
        def evening_slot_constraint(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass


        @staticmethod
        def age_group_constraint(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            pass
        

        @staticmethod
        def meeting_constraint(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            for slot_id in Environment.GAME_SLOT_ID_TO_OBJ | Environment.PRACTICE_SLOT_ID_TO_OBJ:
                activity_type, weekday, start_time = slot_id
                if (weekday == Weekday.TU and start_time in ["11:00", "12:00"]):
                    if (activity_type == ActivityType.GAME 
                        and len(schedule.tues_games[slot_id]) > 0
                    ):
                        return False
                    if (activity_type == ActivityType.PRACTICE 
                        and len(schedule.tues_practices[slot_id]) > 0
                    ):
                        return False
            
            return True
        

        @staticmethod
        def special_bookings_constraint(
            schedule: Schedule, 
            latest_assignment: "tuple[str, tuple[ActivityType, Weekday, str]]"
        ) -> bool:
            "CMSA U12T1S", "CMSA U13T1S"