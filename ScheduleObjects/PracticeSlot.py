
from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType, Weekday
from ScheduleObjects.ActivitySlot import ActivitySlot

class PracticeSlot(ActivitySlot):

    ACTIVITY_TYPE = ActivityType.PRACTICE

    def __init__(self, weekday: Weekday, start_time: str, end_time: str, is_evening_slot: bool, practicemax: int, practicemin: int):
        self.weekday = weekday
        self.id = (self.ACTIVITY_TYPE, weekday, start_time)
        self.start_time = start_time
        self.end_time = end_time
        self.is_evening_slot = is_evening_slot
        self.practicemax= practicemax
        self.practicemin = practicemin

        self.overlaps = set()
    

    def update_overlaps(self):
        pass
