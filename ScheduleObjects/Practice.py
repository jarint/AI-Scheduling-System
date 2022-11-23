'''
This class is used to represent a practice that can be placed somewhere in the schedule
'''

from ScheduleObjects.Activity import Activity


class Practice(Activity):

    def __init__(self, id: str, division: int, association: str, age: str, tier: str, prac: str):
        self.id = id
        self.association = association
        self.age = age
        self.tier = tier
        self.division = division 
        self.prac = prac
    
    def __getID(self):
        return self.id
    
    def __getDivision(self):
        return self.division
    
    def __getAssociation(self):
        return self.association
    
    def __getAge(self):
        return self.age
    
    def __getTier(self):
        return self.tier
    
    def __getPrac(self):
        return self.prac
        self.association = association
        self.age = age
        if tier == '': self.tier = None
        self.division = division
        self.team_num = team_num
        