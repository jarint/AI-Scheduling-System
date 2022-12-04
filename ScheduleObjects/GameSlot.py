
from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType, Weekday
from ScheduleObjects.ActivitySlot import ActivitySlot

class GameSlot(ActivitySlot):

    ACTIVITY_TYPE = ActivityType.GAME

    def __init__(self, weekday: Weekday, start_time: str, end_time: str, is_evening_slot: bool, gamemax: int, gamemin: int):
        self.weekday = weekday
        self.id = (self.ACTIVITY_TYPE, weekday, start_time)
        self.start_time = start_time
        self.end_time = end_time
        self.is_evening_slot = is_evening_slot
        self.gamemax = gamemax
        self.gamemin = gamemin

        self.overlaps = set()
    

    def update_overlaps(self):
        pass
