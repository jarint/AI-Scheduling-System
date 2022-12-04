'''
The methods placed herein will evaluate schedules for their soft constraint compliance and assign penalty scores to each schedule
in our tree as it is generated.

'''

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
        passes = passes and SoftConstraints.CityConstraints.check_city_constraint()
        return passes
    
    class GeneralConstraints:
        @staticmethod
        def check_game_constraints(schedule: Schedule, game: Game, slot: GameSlot):
            pass

        @staticmethod
        def check_practice_constraints(schedule: Schedule, practice: Practice, slot: PracticeSlot):
            pass

        @staticmethod
        def game_min(schedule: Schedule, latest_assignment: tuple):
            activity_id, slot_id = latest_assignment
            activity_type, weekday, start_time = slot_id
            


        @staticmethod
        def practice_min():
            pass

        @staticmethod
        def preference():
            pass

        @staticmethod
        def pair():
            pass

    class CityConstraints:
        @staticmethod
        def check_city_constraint():
            pass
        
        @staticmethod
        def age_tier_constraint():
            pass
    