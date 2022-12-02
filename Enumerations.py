
from enum import Enum


class ActivityType(Enum):
    GAME = "GAME"
    PRACTICE = "PRACTICE"


class Weekday(Enum):
    MO = "MO"
    TU = "TU"
    FR = "FR"


class EnumValueToObjMaps:
    ACTIVITY_TYPES = {activity_type.value: activity_type for activity_type in ActivityType}
    WEEKDAYS = {weekday.value: weekday for weekday in Weekday}





