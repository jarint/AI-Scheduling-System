'''
The class 'Slot' is the object that gets placed into the generated schedules. There are two types of slots
corresponding to games and practices, which will both have attributes of this class.

'''

from abc import ABC, abstractmethod
from ScheduleObjects.Activity import Activity

class ActivitySlot(ABC):
    pass