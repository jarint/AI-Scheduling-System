'''
This class uses objects of the class 'Slot' to build schedules that can be processed by the constraint handling classes
and placed into the tree structure generated by the Tree class. Every object in the schedule must be of the class 'Slot'.

'''

from Search.Environment import Environment
from Enumerations import ActivityType, Weekday


class Schedule:

    def __init__(self) -> None:
        self.__initialize_schedule_dicts()

    
    def get_activities_in_slot(self, slot_id: "tuple[ActivityType, Weekday, str]") -> "set[str]":
        schedule_dict = self.__slot_id_to_schedule_dict(slot_id)
        return self.assignments[slot_id]

        

    def assign_game(self, game_id: str, slot_id: "tuple[ActivityType, Weekday, str]"):
        schedule_dict = self.__slot_id_to_schedule_dict(slot_id)
        schedule_dict[slot_id].add(game_id)


    def assign_practice(self, practice_id: str, slot_id: "tuple[ActivityType, Weekday, str]"):
        schedule_dict = self.__slot_id_to_schedule_dict(slot_id)
        schedule_dict[slot_id].add(practice_id)


    def __initialize_schedule_dicts(self):
        self.mon_games = {slot_id: set() for slot_id in filter(
            lambda id: id[1] == Weekday.MO, Environment.GAME_SLOT_ID_TO_OBJ
        )}
        self.tues_games = {slot_id: set() for slot_id in filter(
            lambda id: id[1] == Weekday.TU, Environment.GAME_SLOT_ID_TO_OBJ
        )}
        
        self.mon_practices = {slot_id: set() for slot_id in filter(
            lambda id: id[1] == Weekday.MO, Environment.PRACTICE_SLOT_ID_TO_OBJ
        )}

        self.tues_practices = {slot_id: set() for slot_id in filter(
            lambda id: id[1] == Weekday.TU, Environment.PRACTICE_SLOT_ID_TO_OBJ
        )}

        self.fri_practices = {slot_id: set() for slot_id in filter(
            lambda id: id[1] == Weekday.FR, Environment.PRACTICE_SLOT_ID_TO_OBJ
        )}


    def __slot_id_to_schedule_dict(self, slot_id: "tuple[ActivityType, Weekday, str]"):
        TYPE_AND_DAY_TO_ARR = {
            (ActivityType.GAME, Weekday.MO): self.mon_games,
            (ActivityType.GAME, Weekday.TU): self.tues_games,
            (ActivityType.PRACTICE, Weekday.MO): self.mon_practices,
            (ActivityType.PRACTICE, Weekday.TU): self.tues_practices,
            (ActivityType.PRACTICE, Weekday.FR): self.fri_practices
        }
        activity_type, weekday, time_str = slot_id
        type_and_day = (activity_type, weekday)
        try:
            schedule_dict = TYPE_AND_DAY_TO_ARR[type_and_day]
        except KeyError:
            raise ValueError("slot type or day is invalid.")

        return schedule_dict