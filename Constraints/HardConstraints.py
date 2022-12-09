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
    def check_constraints(schedule: Schedule, assignment: tuple): # TODO: add type of 'assignment' parameter
        # Index 1 of assignment is the slot ID, so index 0 of that is the activity type
        activity_type = assignment[1][0]

        # Type of activity should be GAME or PRACTICE
        if (not((activity_type == ActivityType.GAME) or (activity_type == ActivityType.PRACTICE))):
            raise TypeError("Activity given to 'check_constraints' method in HardConstraints must be either of type 'Game' or type 'Practice'")

        return (
            HardConstraints.GeneralConstraints.check_general_constraints(schedule, assignment) and
            HardConstraints.CityConstraints.check_city_constraints(schedule, assignment)
        )


    # TODO: update all constraint check methods to use 'assignment' as second parameter instead of 'schedule.latest_assignment'
        # note that assignment[0] is an activity ID (str) and assignment[1] is a slot ID (tuple)
            # slot_id[0] is an activity type (ActivityType), slot_id[1] is a weekday (Weekday), and slot_id[2] is a start time (str)
                # the ActivityType and WeekDay classes can be found in Enumerations.py


    class GeneralConstraints:
        @staticmethod
        def check_general_constraints(schedule: Schedule, assignment: tuple) -> bool:
            """
            Assumes that the activity type of the activity in 'assignment' is of type GAME or PRACTICE
            """
            activity_type = assignment[1][0]

            if (activity_type == ActivityType.GAME): # activity is a game
                passes = HardConstraints.GeneralConstraints.game_max(schedule, assignment)
            else: # activity is a practice
                passes = HardConstraints.GeneralConstraints.practice_max(schedule, assignment)

            # The additional constraints below are checked whether the activity is a game or a practice
            return passes and (
                HardConstraints.GeneralConstraints.gp_same_slot(schedule, assignment) and
                HardConstraints.GeneralConstraints.part_assign(schedule, assignment) and
                HardConstraints.GeneralConstraints.unwanted(schedule, assignment)
            )


        @staticmethod
        def game_max(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            activity_type = slot_id[0]
            slot_obj = Environment.SLOT_ID_TO_OBJ[slot_id]
            if activity_type != ActivityType.GAME:
                return True
            if len(schedule.assignments[slot_id]) >= slot_obj.gamemax:
                return False
            return True


        @staticmethod
        def practice_max(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            activity_type = slot_id[0]
            slot_obj = Environment.SLOT_ID_TO_OBJ[slot_id]
            if activity_type != ActivityType.PRACTICE:
                return True
            if len(schedule.assignments[slot_id]) >= slot_obj.practicemax:
                return False
            return True


        # Game/practice same slot assignment
        @staticmethod
        def gp_same_slot(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            slot_obj = Environment.SLOT_ID_TO_OBJ[slot_id]
            overlapping_slots = slot_obj.overlaps
            activity_obj = Environment.ACTIVITY_ID_TO_OBJ[activity_id]
            type_a = activity_obj.ACTIVITY_TYPE

            for overlapping_slot in overlapping_slots:
                for act_id in schedule.assignments[overlapping_slot]:
                    act_obj = Environment.ACTIVITY_ID_TO_OBJ[act_id]
                    type_b = act_obj.ACTIVITY_TYPE
                    if type_a == ActivityType.PRACTICE and type_b == ActivityType.PRACTICE:
                        continue
                    
                    # TODO unsure of which implementation is correct
                    # implementation version 1 
                    same_assoc = (activity_obj.association == act_obj.association)
                    same_age = (activity_obj.age == act_obj.age)
                    same_tier = (activity_obj.tier == act_obj.tier)
                    same_division = (activity_obj.division == act_obj.division)
                    if same_assoc and same_age and same_tier and same_division:
                        return False

                    # implementation version 2
                    # if activity_obj.division == act_obj.division:
                    #     return False

            return True


        # Not compatible assignment
        @staticmethod
        def not_compatible(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            for id in schedule.assignments[slot_id]:
                if Environment.NOT_COMPATIBLE[activity_id].contains(id): 
                    return False
            return True


        # Partial assignment
        @staticmethod
        def part_assign(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            if activity_id not in Environment.PARTASSIGN:
                return True
            return slot_id == Environment.PARTASSIGN[activity_id]


        # Unwanted assignment
        @staticmethod
        def unwanted(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            for slot in Environment.UNWANTED[activity_id]:
                if slot_id == slot:
                    return False
            
            return True


    class CityConstraints:
        
        @staticmethod
        def check_city_constraints(schedule: Schedule, assignment: tuple) -> bool:
            """
            Assumes that the activity type of the activity in 'assignment' is of type GAME or PRACTICE
            """
            activity_id, slot_id = assignment
            activity_type = slot_id[0]

            if (activity_type == ActivityType.GAME): # activity is a game
                passes = (
                    HardConstraints.CityConstraints.age_group_constraint(schedule, assignment) and
                    # HardConstraints.CityConstraints.meeting_constraint(schedule, assignment) and
                    HardConstraints.CityConstraints.special_bookings_constraint(schedule, assignment)
                )
            else: # activity is a practice
                passes = True

            if Environment.ACTIVITY_ID_TO_OBJ[activity_id].division is not None:
                passes = passes and HardConstraints.CityConstraints.evening_slot_constraint(schedule, assignment)

            # The additional constraints below are checked whether the activity is a game or a practice
            return passes


        @staticmethod
        def evening_slot_constraint(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            activity_obj = Environment.ACTIVITY_ID_TO_OBJ[activity_id]
            if (activity_obj.division == 9): # TODO may not only be division 9, but divisions that start with 9
                return not Parser.decide_if_evening_slot(slot_id[2])
            else:
                return True


        @staticmethod
        def age_group_constraint(schedule: Schedule, assignment: tuple) -> bool:
            MUTEX_AGES = {"U15", "U16", "U17", "U19"}

            activity_id, slot_id = assignment
            activity_type = slot_id[0]
            if activity_type != ActivityType.GAME:
                return True # this hard constraint only involves games
            
            age_a = Environment.GAME_ID_TO_OBJ[activity_id].age
            if age_a not in MUTEX_AGES:
                return True

            for act_id in schedule.assignments[slot_id]:
                if act_id == activity_id:
                    continue
                
                age_b = Environment.GAME_ID_TO_OBJ[act_id].age
                if age_b in MUTEX_AGES:
                    return False
            
            return True


        # NOTE May be better to include the Tuesday meeting slot, but assign it a game min/max of 0
            # this is now in Environment.post_parser_initialization()

        # @staticmethod
        # def meeting_constraint(schedule: Schedule, assignment: tuple) -> bool:
        #     activity_id, slot_id = assignment
        #     activity_type, weekday, start_time = slot_id
        #     if weekday != Weekday.TU:
        #         return True
        #     if start_time not in ["11:00", "12:00"]:
        #         return True
        #     if len(schedule.assignments[slot_id]) == 0:
        #         return True
        #     return False
        

        # TODO: May be issues with this constraint and it may be incomplete.
            # CMSA U12T1S and CMSA U13T1S are GAMES not practices
                # And they must be in TU "18:00" slot
            # Also, CMSC U12T1S is not allowed to overlap with any practices/games of CMSC U12T1
            # Also, CMSC U13T1S is not allowed to overlap with any practices/games of CMSC U13T1
        # One other note: U12T1S and U13T1S won't actually be given in the input, but rather, we should infer their existence if their non-special conterparts are given
            # The parser will implement this
            # If we parse U13T1 as an input game, then we will also add its special counterpart as a game
                # The same applies to U12T1

        # NOTE issue resolved 
            # the way I have it implemented now is that they are games placed in practice slots

        @staticmethod
        def special_bookings_constraint(schedule: Schedule, assignment: tuple) -> bool:
            activity_id, slot_id = assignment
            act_obj = Environment.ACTIVITY_ID_TO_OBJ[activity_id]

            if act_obj.ACTIVITY_TYPE != ActivityType.GAME:
                return True # this constraint doesn't apply to practices

            association, age, tier = act_obj.association, act_obj.age, act_obj.tier

            if association != "CMSA" or age not in {"U12", "U13"} or tier != "T1":
                return True # constraint doesn't apply to this given game


            if activity_id in Environment.SPECIAL_BOOKINGS:
                if slot_id == Environment.SPECIAL_BOOKINGS[activity_id]:
                    return True
                
                return False
            
            # at this point in the hard constraint check, we've narrowed it down that we're dealing with a game
            # that isn't one of the special games, but shares the association, age and tier of one of them.
            if age == "U12":
                if "CMSA U12T1S" in schedule.assignments[slot_id]:
                    return False
                return True
            elif age == "U13":
                if "CMSA U13T1S" in schedule.assignments[slot_id]:
                    return False
                return True
            else:
                raise Exception("age should be one of U12 or U13 at this point in the hard constraint check")
                        
