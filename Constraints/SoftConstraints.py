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
from Enumerations import ActivityType

class SoftConstraints:


    # TODO: determine if we can compute the penalty values of the new assignment, or if we need to recompute for the whole schedule
        # Do we need to recalculate? Or can we simply add the change in the penalty value that the new assignment causes?


    @staticmethod
    def get_delta_eval(schedule: Schedule, latest_assignment: tuple) -> int:
        delta_eval_minfilled_games = SoftConstraints.GeneralConstraints.game_min(schedule, latest_assignment) * Environment.W_MINFILLED
        delta_eval_minfilled_practices = SoftConstraints.GeneralConstraints.practice_min(schedule, latest_assignment) * Environment.W_MINFILLED
        delta_eval_pref = SoftConstraints.GeneralConstraints.preference(schedule, latest_assignment) * Environment.W_PREF
        delta_eval_pair = SoftConstraints.GeneralConstraints.pair(schedule, latest_assignment) * Environment.W_PAIR
        delta_eval_secdiff = SoftConstraints.check_city_constraint(schedule, latest_assignment) * Environment.W_SECDIFF

        return sum(
            delta_eval_minfilled_games,
            delta_eval_minfilled_practices,
            delta_eval_pref,
            delta_eval_pair,
            delta_eval_secdiff
        )
    
    
    class GeneralConstraints:

        @staticmethod
        def game_min(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            activity_type = slot_id[0]
            if activity_type == ActivityType.PRACTICE:
                return 0
            slot_obj = Environment.GAME_SLOT_ID_TO_OBJ[slot_id]
            penatly_included = len(schedule.assignments[slot_id]) < slot_obj.gamemin
            delta_penalty = 0
            if penatly_included:
                delta_penalty = -1 * Environment.PEN_GAMEMIN # reducing penalty value
            return delta_penalty
            

        @staticmethod
        def practice_min(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            activity_type = slot_id[0]
            if activity_type == ActivityType.GAME:
                return 0
            slot_obj = Environment.PRACTICE_SLOT_ID_TO_OBJ[slot_id]
            penalty_included = len(schedule.assignments[slot_id]) < slot_obj.practicemin
            delta_penalty = 0
            if penalty_included:
                delta_penalty = -1 * Environment.PEN_PRACTICEMIN # reducing penalty value
            return delta_penalty


        @staticmethod
        def preference(schedule: Schedule, latest_assignment: tuple) -> int:
            activity_id, slot_id = latest_assignment
            delta_penalty = 0

            for preference in Environment.PREFERENCES[activity_id]:
                pref_slot_id, pref_value = preference
                if slot_id == pref_slot_id:
                    delta_penalty -= pref_value
            
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
        activity_type = slot_id[0]
        if activity_type == ActivityType.PRACTICE:
            return 0
        delta_penalty = 0
        activity_obj = Environment.GAME_ID_TO_OBJ[activity_id]
        age, tier = activity_obj.age, activity_obj.tier
        for act_id in schedule.assignments[slot_id]:
            act_obj = Environment.GAME_ID_TO_OBJ[act_id]
            a, t = act_obj.age, act_obj.tier
            if a == age and t == tier:
                delta_penalty += Environment.PEN_SECTION
        return delta_penalty