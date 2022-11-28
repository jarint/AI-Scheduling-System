'''
This class uses objects of the class 'Slot' to build schedules that can be processed by the constraint handling classes
and placed into the tree structure generated by the Tree class. Every object in the schedule must be of the class 'Slot'.

'''

from Search.Environment import Environment
from Enumerations import ActivityType, Weekday


class Schedule:

    def __init__(self) -> None:
        self.assignments = {slot_id: set() for slot_id in Environment.ALL_SLOT_IDS}

    
    def get_activities_in_slot(self, slot_id: "tuple[ActivityType, Weekday, str]") -> "set[str]":
        return self.assignments[slot_id]
        

    def assign_game(self, game_id: str, slot_id: "tuple[ActivityType, Weekday, str]"):
        schedule_dict = self.__slot_id_to_schedule_dict(slot_id)
        self.assignments[slot_id].add(game_id)


    def assign_practice(self, practice_id: str, slot_id: "tuple[ActivityType, Weekday, str]"):
        self.assignments[slot_id].add(practice_id)