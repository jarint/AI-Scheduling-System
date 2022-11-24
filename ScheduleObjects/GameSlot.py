
from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType, Weekday
from ScheduleObjects.ActivitySlot import ActivitySlot

class GameSlot(ActivitySlot):

    ACTIVITY_TYPE = ActivityType.GAME

    def __init__(self, weekday: Weekday, time_str: str, start_time: str, duration: str, is_evening_slot: bool):
        self.weekday = weekday
        self.time_str = time_str
        self.id = (self.ACTIVITY_TYPE, weekday, time_str)

        self.start_time = start_time
        self.end_time = start_time + duration
        self.duration = duration
        self.is_evening_slot = is_evening_slot

        self.overlaps = []
        self.__update_overlaps()
    

    def __update_overlaps():
        pass
