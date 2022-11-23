

from ScheduleObjects.Activity import Activity
from ScheduleObjects.ActivitySlot import ActivitySlot

class PracticeSlot(ActivitySlot):
    def __init__(self, slot_num: int, days: str, start_time: str, length: str):
        self.id = (days, slot_num)
        self.slot_num = slot_num
        self.days = days
        self.start_time = start_time
        self.end_time = start_time + length
        self.length = length
        self.overlaps = []
        self.__update_overlaps()

    def get_activities(self):
        return self.activities
    
    def __update_overlaps():
        pass
