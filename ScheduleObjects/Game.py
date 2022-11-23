'''
This class is used to represent a game that can be placed somewhere in the schedule
'''

from ScheduleObjects.Activity import Activity


class Game(Activity):

    def __init__(self, id: str, association: str, age: str, tier: str, division: int):
        self.id = id
        self.association = association
        self.age = age
        self.tier = tier
        self.division = division
        