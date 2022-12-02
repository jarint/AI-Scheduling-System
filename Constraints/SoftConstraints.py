'''
The methods placed herein will evaluate schedules for their soft constraint compliance and assign penalty scores to each schedule
in our tree as it is generated.

'''

from ScheduleObjects.Activity import Activity
from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.ActivitySlot import Slot

class SoftConstraints:

    @staticmethod
    def check_constraints(schedule: Schedule, activity: Activity, slot: Slot):
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
        def check_game_constraints(schedule: Schedule, game: Game, slot: Slot):
            pass

        @staticmethod
        def check_practice_constraints(schedule: Schedule, practice: Practice, slot: Slot):
            pass

        @staticmethod
        def game_min():
            pass

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
    