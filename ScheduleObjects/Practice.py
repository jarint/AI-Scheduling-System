'''
This class is used to represent a practice that can be placed somewhere in the schedule
'''

from ScheduleObjects.Activity import Activity


class Practice(Activity):

    def __init__(self, id: str, association: str, age: str, tier: str, division: int, team_num: int):
        self.id = id
        self.association = association
        self.age = age
        if tier == '': self.tier = None
        self.division = division
        self.team_num = team_num