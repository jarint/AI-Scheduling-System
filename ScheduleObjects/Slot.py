'''
The class 'Slot' is the object that gets placed into the generated schedules. There are two types of slots
corresponding to games and practices, which will both have attributes of this class.

'''

from ScheduleObjects.Activity import Activity

class Slot:
    activities = []

    def __init__(self, start_time: str, end_time: str, evening_slot: bool):
        self.start_time = start_time
        self.end_time = end_time
        self.evening_slot = evening_slot

    def add_activity(self, activity: Activity):
        self.activities.append(activity)

    def get_activities(self):
        return self.activities
