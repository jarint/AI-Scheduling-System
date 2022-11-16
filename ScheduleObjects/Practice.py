'''
This class is used to represent a practice that can be placed somewhere in the schedule
'''

from ScheduleObjects.Activity import Activity


class Practice(Activity):

    def __init__(self, id: str, division: int, team: int):
        self.id = id
        