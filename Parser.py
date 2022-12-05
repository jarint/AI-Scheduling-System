'''
This class parses the input files for the decision problem and loads the information therein to data structures and objects
that can be used by the AI to generate a schedule.

'''

import sys
import logging
import os
import re

from Search.Environment import Environment
from Enumerations import ActivityType, Weekday
from ScheduleObjects.Game import Game
from ScheduleObjects.ActivitySlot import ActivitySlot
from ScheduleObjects.Practice import Practice
from ScheduleObjects.GameSlot import GameSlot
from ScheduleObjects.PracticeSlot import PracticeSlot
from Enumerations import EnumValueToObjMaps

from copy import deepcopy


class Parser:
    FILE_HEADINGS = [
        "Name:",
        "Game slots:",
        "Practice slots:",
        "Games:",
        "Practices:",
        "Not compatible:",
        "Unwanted:",
        "Preferences:",
        "Pair:",
        "Partial assignments:",

        "LAST_HEADING_ENTRY"
    ]


    COMMA_REGEX = r"\s*,\s*"


    def __init__(self) -> None:
        Environment.pre_parser_initialization()
        self.__parse_commandline_args()
        self.__parse_file()
        Environment.post_parser_initialization()


    def __next_line(self) -> str:
        if (self.current_line == self.num_lines):
            return None # end of file

        next_line = self.file_contents[self.current_line]
        while (next_line.strip() == ""):
            self.current_line += 1
            if (self.current_line == self.num_lines):
                return None # end of file
            next_line = self.file_contents[self.current_line]

        if (self.FILE_HEADINGS[self.current_heading_index + 1] in next_line):
            self.current_heading_index += 1
            self.current_line += 1
            return None # end of section

        self.current_line += 1
        self.line_str = next_line.strip()
        logging.debug("    " + str(next_line.strip()))
        return next_line


    def __parse_commandline_args(self) -> None:
        logging.debug("__parse_commandline_args")
        args = sys.argv
        self.__validate_args(args)
        
        self.filename = args[1]
        (
            Environment.W_MINFILLED,
            Environment.W_PREF,
            Environment.W_PAIR,
            Environment.W_SECDIFF,
            Environment.PEN_GAMEMIN, 
            Environment.PEN_PRACTICEMIN, 
            Environment.PEN_NOTPAIRED, 
            Environment.PEN_SECTION
        ) = (int(arg) for arg in args[2:])

        
    def __validate_args(self, args):
        valid = True

        print(len(args))

        # Should be 10 command line arguments
        if len(args) != 10:
            valid = False
        else:
            # Second argument should be a valid input filename (first is irrelevent)
            if not(os.path.exists(args[1])): valid = False

            # The third argument and those thereafter should be integers
            for arg in args[2:]:
                try:
                    int(arg)
                except ValueError:
                    valid = False

        # If the command line arguments are invalid we raise a runtime exception for debugging purposes
        if not(valid): raise RuntimeError("Command line arguments must contain a valid filename, four integer weights (min filled, pref, pair, sec diff), and four integer penalty values(game min, practice min, not paired, section)")
    
    # <file parsing methods>

    def __parse_file(self) -> None:
        logging.debug("__parse_file")
        with open(self.filename, "r") as fh:
            self.file_contents = fh.readlines()
            self.num_lines = len(self.file_contents)
            self.current_line = 0
            self.current_heading_index = 0
            self.line_str = ""
        
        self.__parse_name()
        self.__parse_game_slots()
        self.__parse_practice_slots()
        self.__parse_games()
        self.__parse_practices()
        self.__parse_not_compatible()
        self.__parse_unwanted()
        self.__parse_preferences()
        self.__parse_pairs()
        self.__parse_partial_assignments()


    def __parse_name(self) -> None:
        logging.debug("  __parse_name")
        while (self.__next_line() is not None):
            line = self.line_str
            Environment.NAME = line


    def __parse_game_slots(self) -> None:
        logging.debug("  __parse_game_slots")
        while (self.__next_line() is not None):
            line = self.line_str
            game_slot = self.__parse_game_slot(line)
            Environment.Adders.add_game_slot(game_slot)


    def __parse_practice_slots(self) -> None:
        logging.debug("  __parse_practice_slots")
        while (self.__next_line() is not None):
            line = self.line_str
            practice = self.__parse_practice_slot(line)
            Environment.Adders.add_practice_slot(practice)


    # TODO: U13T1S won't actually be given in the input, but rather, we should infer its existence if U13T1 is given as input
        # Though this is not necessarily something we will implement here
        # Instead, if we parse U13T1 as an input game, then we will also add its special counterpart as a practice
            # I believe the same applies to U12T1
    def __parse_games(self) -> None:
        logging.debug("  __parse_games")
        while (self.__next_line() is not None):
            line = self.line_str
            game = self.__parse_game_id(line)
            Environment.Adders.add_game(game)

            if ((game.age == "U12" or game.age == "U13") and game.tier == "T1"):
                special_game = deepcopy(game)
                special_game.id = special_game.id + "S"
                Environment.Adders.add_practice(Practice(game.association + " " + game.age + game.tier + "S", game.association, game.age, None, None))


    def __parse_practices(self) -> None:
        logging.debug("  __parse_practices")

        # special bookings (this is a city of calgary hard constraint that requires these special practices)
        special_a = Practice("CMSA U12T1S", "CMSA", "U12", "1", None, None)
        special_b = Practice("CMSA U13T1S", "CMSA", "U13", "1", None, None)
        Environment.Adders.add_practice(special_a)
        Environment.Adders.add_practice(special_b)

        while (self.__next_line() is not None):
            line = self.line_str
            practice = self.__parse_practice_id(line)
            Environment.Adders.add_practice(practice)


    def __parse_not_compatible(self):
        while (self.__next_line() is not None):
            line = self.line_str
            activity_1, activity_2 = re.split(self.COMMA_REGEX, line)
            Environment.Adders.add_not_compatible(activity_1, activity_2)
        

    def __parse_unwanted(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str
            activity_id, date, time = re.split(self.COMMA_REGEX, line)

            print("======================")
            print(activity_id)
            print(Environment.ACTIVITY_IDS)
            print("======================")

            if activity_id in Environment.GAME_IDS:
                activity_type = ActivityType.GAME
            elif activity_id in Environment.PRACTICE_IDS:
                activity_type = ActivityType.PRACTICE
            else:
                raise(RuntimeError("Unwanted ID not found in game IDs or practice IDs"))
            
            if (date == 'MO'):
                date_enum = Weekday.MO
            elif (date == 'TU'):
                date_enum = Weekday.TU
            elif (date == 'FR'):
                date_enum = Weekday.FR
            slot = (activity_type, date_enum, time)
            Environment.Adders.add_unwanted(activity_id, slot)


    def __parse_preferences(self) -> None:
        logging.debug("  __parse_preferences")
        while (self.__next_line() is not None):
            line = self.line_str
            preference = self.__parse_preference(line)
            activity_id, slot_id, pref_value = preference
            Environment.Adders.add_preference(preference)
        
        # assign default value of 0 if unspecified
        for slot_id in Environment.ALL_SLOT_IDS:
            for activity_id in Environment.ACTIVITY_IDS:
                if (slot_id, activity_id) not in Environment.PREFERENCES:
                    Environment.PREFERENCES[activity_id] = (slot_id, 0)


    def __parse_pairs(self) -> None:
        logging.debug("  __parse_pairs")
        for activity_id in Environment.GAME_ID_TO_OBJ | Environment.PRACTICE_ID_TO_OBJ:
            Environment.PAIR[activity_id] = set()

        while (self.__next_line() is not None):
            line = self.line_str
            pair = re.split(self.COMMA_REGEX, line)
            Environment.Adders.add_pair(pair)
            

    def __parse_partial_assignments(self) -> None:
        logging.debug("  __parse_partial_assignments")
        while (self.__next_line() is not None):
            line = self.line_str
            itemized = re.split(self.COMMA_REGEX, line)
            activity_id = itemized[0]
            activity_type = self.decide_activity_type(itemized[0])
            weekday = EnumValueToObjMaps.WEEKDAYS[itemized[1]]
            time_str = itemized[2]
            slot_id = (activity_type, weekday, time_str)
            Environment.Adders.add_partassign((activity_id, slot_id))


    # </file parsing methods>

    
    # <lower level parsing helpers>
            

    def __parse_activity_id(self, activity_id: str) -> None:
        activity_type = self.decide_activity_type(activity_id)
        if activity_type == ActivityType.GAME:
            return self.__parse_game_id(activity_id)
        elif activity_type == ActivityType.PRACTICE:
            return self.__parse_practice_id(activity_id)
        else:
            raise Exception("Invalid activity type in Parser.__parse_activity_id()")


    def __parse_game_id(self, game_id: str) -> Game:
        # Splitting game identifier
        split_id = game_id.split(' ')
        split_id[:] = [x for x in split_id if x] # removing empty strings in case there were extra spaces

        if len(split_id) != 4: raise RuntimeError("Issue parsing game '" + game_id + "': split does not result in four elements")

        association = split_id[0]

        # Parsing age and tier
        age_tier = split_id[1].split('T')
        age = age_tier[0]
        if len(age_tier) == 2: tier = 'T' + age_tier[1]
        else: tier = None

        division = int(split_id[3])

        return Game(game_id, association, age, tier, division)


    def __parse_practice_id(self, practice_id: str) -> Practice:
        # Splitting practice identifier
        split_id = practice_id.split(' ')
        split_id[:] = [x for x in split_id if x] # removing empty strings in case there were extra spaces

        print("=======================================")
        print(split_id)
        print("=======================================")

        if not(len(split_id) == 4 or len(split_id) == 6): raise RuntimeError("Issue parsing practice '" + practice_id + "': split does not result in four or six elements")

        association = split_id[0]

        # Parsing age and tier
        age_tier = split_id[1].split('T')
        age = age_tier[0]
        if len(age_tier) == 2: tier = 'T' + age_tier[1]
        else: tier = None

        if len(split_id) == 4: # only four strings resulting from splut: no division
            division = None
            practice_num = int(split_id[3])
        else: # six strings resulting from splut: division given
            division = int(split_id[3])
            practice_num = int(split_id[5])

        return Practice(practice_id, association, age, tier, division, practice_num)


    def __parse_game_slot(self, game_slot_name: str) -> GameSlot:
        split_line = re.split(self.COMMA_REGEX, game_slot_name)
        weekday_name = split_line[0]
        weekday = EnumValueToObjMaps.WEEKDAYS[weekday_name]
        start_time = split_line[1]
        gamemax = int(split_line[2])
        gamemin = int(split_line[3])
        is_evening_slot = self.decide_if_evening_slot(start_time)

        # TODO: compute end_time and use as input when creating a new game slot

        return GameSlot(weekday=weekday, start_time=start_time, end_time="", gamemax=gamemax, gamemin=gamemin, is_evening_slot=is_evening_slot)


    def __parse_practice_slot(self, practice_slot_name: str) -> PracticeSlot:
        split_line = re.split(self.COMMA_REGEX, practice_slot_name)
        weekday_name = split_line[0]
        weekday = EnumValueToObjMaps.WEEKDAYS[weekday_name]
        start_time = split_line[1]
        practicemax = int(split_line[2])
        practicemin = int(split_line[3])
        is_evening_slot = self.decide_if_evening_slot(start_time)

        # TODO: compute end_time and use as input when creating a new game slot

        return PracticeSlot(weekday=weekday, start_time = start_time, end_time="", practicemax=practicemax, practicemin=practicemin, is_evening_slot=is_evening_slot)

    def time_str_to_int(self, time_str: str) -> int:
        try:
            hours, mins = (int(e) for e in time_str.strip().split(":"))
        except ValueError:
            raise ValueError(f"invalid time string: {time_str}")
        
        return hours * 60 + mins

    def decide_if_evening_slot(self, time_str: str) -> bool:
        time_int = self.time_str_to_int(time_str)
        return time_int >= 1080 # 18:00 - 18 * 60 = 1080
    
    def decide_activity_type(self, activity_id: str) -> ActivityType:
        for phrase in ["PRC", "OPN", "CMSA U12T1S", "CMSA U13T1S"]:
            if phrase in activity_id:
                return ActivityType.PRACTICE
        
        return ActivityType.GAME


    def __parse_preference(self, preference_str: str) -> "tuple[tuple[ActivityType, Weekday, str], str, int]":
        try:
            itemized = re.split(self.COMMA_REGEX, preference_str)
            activity_type = self.decide_activity_type(itemized[2])
            weekday = EnumValueToObjMaps.WEEKDAYS[itemized[0]]
            start_time = itemized[1]
            slot_id = (activity_type, weekday, start_time)
            activity_id = itemized[2]
            pref_value = int(itemized[3])
        except ValueError:
            raise ValueError(f"invalid preference string {preference_str}")

        return (slot_id, activity_id, pref_value)



    # </lower level parsing helpers>
