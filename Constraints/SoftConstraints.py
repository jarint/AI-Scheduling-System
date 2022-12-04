'''
The methods placed herein will evaluate schedules for their soft constraint compliance and assign penalty scores to each schedule
in our tree as it is generated.

'''

from Search.Environment import Environment
from ScheduleObjects.Activity import Activity
from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.ActivitySlot import ActivitySlot
from ScheduleObjects.GameSlot import GameSlot
from ScheduleObjects.PracticeSlot import PracticeSlot

class SoftConstraints:


    # TODO: determine if we can compute the penalty values of the new assignment, or if we need to recompute for the whole schedule
        # Do we need to recalculate? Or can we simply add the change in the penalty value that the new assignment causes?


    @staticmethod
    def check_constraints(schedule: Schedule, activity: Activity, slot: ActivitySlot):
        passes = True
        if (isinstance(activity, Game)):
            passes = passes and SoftConstraints.GeneralConstraints.check_game_constraints()
        elif (isinstance(activity, Practice)):
            passes = passes and SoftConstraints.GeneralConstraints.check_practice_constraints()
        else:
            raise TypeError("Activity given to 'check_constraints method must be either of type 'Game' or type 'Practice'")
        passes = passes and SoftConstraints.check_city_constraint()
        return passes
    
    
    class GeneralConstraints:

        @staticmethod
        def check_game_constraints(schedule: Schedule, latest_assignment: tuple):
            # TODO not sure if this method needs to exist
            pass


        @staticmethod
        def check_practice_constraints(schedule: Schedule, latest_assignment: tuple):
            # TODO not sure if this method needs to exist
            pass


        @staticmethod
        def game_min(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            slot_obj = Environment.SLOT_ID_TO_OBJ[slot_id]
            penatly_included = len(schedule.assignments[slot_id]) < slot_obj.gamemin
            delta_penalty = 0
            if penatly_included:
                delta_penalty = -1 * Environment.PEN_GAMEMIN # reducing penalty value
            return delta_penalty
            

        @staticmethod
        def practice_min(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            slot_obj = Environment.SLOT_ID_TO_OBJ[slot_id]
            penalty_included = len(schedule.assignments[slot_id]) < slot_obj.practicemin
            delta_penalty = 0
            if penalty_included:
                delta_penalty = -1 * Environment.PEN_PRACTICEMIN # reducing penalty value
            return delta_penalty


        @staticmethod
        def preference(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            delta_penalty = 0
            if activity_id in Environment.PREFERENCES:
                pref_slot_id, preference = Environment.PREFERENCES[activity_id]
                if slot_id != pref_slot_id:
                    delta_penalty = preference
            return delta_penalty


        @staticmethod
        def pair(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            delta_penalty = 0
            if activity_id in Environment.PAIR:
                paired_activities = Environment.PAIR[activity_id]
                for act in paired_activities:
                    if (act in schedule.remaining_games) or (act in schedule.remaining_practices):
                        continue
                    if act not in schedule.assignments[slot_id]:
                        delta_penalty += Environment.PEN_NOTPAIRED
            return delta_penalty


    @staticmethod
    def check_city_constraint(schedule: Schedule, latest_assignment: tuple) -> int:
        activity_id, slot_id = latest_assignment
        delta_penalty = 0
        activity_obj = Environment.ACTIVITY_ID_TO_OBJ[activity_id]
        age, tier = activity_obj.age, activity_obj.tier
        for act_id in schedule.assignments[slot_id]:
            act_obj = Environment.ACTIVITY_ID_TO_OBJ[act_id]
            a, t = act_obj.age, act_obj.tier
            if a == age and t == tier:
                delta_penalty += Environment.PEN_SECTION
        return delta_penalty