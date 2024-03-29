'''
This class is used to represent a practice that can be placed somewhere in the schedule
'''

from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType


class Practice(Activity):

    ACTIVITY_TYPE = ActivityType.PRACTICE

    def __init__(self, id: str, association: str, age: str, tier: str, division: int, practice_num: int):
        self.id = id
        self.association = association
        self.age = age
        self.tier = tier
        self.division = division
        self.practice_num = practice_num
    

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