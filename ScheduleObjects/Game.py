'''
This class is used to represent a game that can be placed somewhere in the schedule
'''

from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType


class Game(Activity):

    ACTIVITY_TYPE = ActivityType.GAME

    def __init__(self, id: str, association: str, age: str, tier: str, division: int):
        self.id = id
        self.association = association
        self.age = age
        self.tier = tier
        self.division = division


    def get_id(self):
        return self.id
    

    def get_association(self):
        return self.association
    

    def get_age(self):
        return self.age
    

    def get_tier(self):
        return self.tier
    

    def get_division(self):
        return self.division