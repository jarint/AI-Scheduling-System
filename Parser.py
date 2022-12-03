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
            Environment.w_minfilled,
            Environment.w_pref,
            Environment.w_pair,
            Environment.w_secdiff,
            Environment.pen_gamemin, 
            Environment.pen_practicemin, 
            Environment.pen_notpaired, 
            Environment.pen_section
        ) = (int(arg) for arg in args[2:])

        
    def __validate_args(self, args):
        valid = True

        # Should be 10 command line arguments
        if len(args) != 10: valid = False

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


    def __parse_games(self) -> None:
        logging.debug("  __parse_games")
        while (self.__next_line() is not None):
            line = self.line_str
            game = self.__parse_game_id(line)
            Environment.Adders.add_game(game)


    def __parse_practices(self) -> None:
        logging.debug("  __parse_practices")

        # special bookings (this is a city of calgary hard constraint that requires these special practices)
        special_a = Practice("CMSA U12T1S", "CMSA", "U12", "1", None)
        special_b = Practice("CMSA U13T1S", "CMSA", "U13", "1", None)
        Environment.Adders.add_practice(special_a)
        Environment.Adders.add_practice(special_b)

        while (self.__next_line() is not None):
            line = self.line_str
            practice = self.__parse_practice_id(line)
            Environment.Adders.add_practice(practice)


    # Returns a list of 2 games of 2 practice object that are not compatible
    def __parse_not_compatible(self, games_and_practices_string: str):
        while (self.__next_line() is not None):
            activity_1, activity_2 = games_and_practices_string.split(', ')
            Environment.Adders.add_not_compatible(activity_1, activity_2)
        

    def __parse_unwanted(self, unwanted_schedule_string) -> None:
        unwanted_id = "str"
        if unwanted_id in Environment.GAME_IDS:
            # is a game
            # turn input into game slot_id
            # add to corresponding list
            pass
        elif unwanted_id in Environment.PRACTICE_IDS:
            # is a practice
            # turn input into practice slot_id
            # add to corresponding list
            pass
        else:
            raise(RuntimeError("Unwanted ID not found in game IDs or practice IDs"))

        #example CSMA U13T3 DIV 01, MO, 8:00
        unwanted_schedule = unwanted_schedule_string.split(', ')
        unwanted_day = unwanted_schedule[1]
        unwanted_time = unwanted_schedule[2]
        unwanted_team_info = unwanted_schedule[0].split(' ')

        if len(unwanted_team_info) > 4:
            team_association = unwanted_team_info[0]
            team_age_and_tier = unwanted_team_info[1].split('T')
            team_age = team_age_and_tier[0]
            team_tier = team_age_and_tier[1]
            team_division = unwanted_team_info[3]
            team_prac = unwanted_team_info[4] + ' ' + unwanted_team_info[5]
            unwanted_team = Practice(unwanted_schedule[0], team_association, team_age, team_tier, team_division, team_prac)
        else:
            team_association = unwanted_team_info[0]
            team_age_and_tier = unwanted_team_info[1].split('T')
            team_age = team_age_and_tier[0]
            team_tier = team_age_and_tier[1]
            team_division = unwanted_team_info[3]
            unwanted_team = Game(team_association, team_age, team_tier, team_division)
        return unwanted_team, unwanted_day, unwanted_time

    def __parse_preferences(self) -> None:
        logging.debug("  __parse_preferences")
        while (self.__next_line() is not None):
            line = self.line_str
            preference = self.__parse_preference(line)
            slot_id, activity_id, pref_value = preference
            Environment.Adders.add_preference(preference)
        
        # assign default value of 0 if unspecified
        for slot_id in Environment.GAME_SLOT_ID_TO_OBJ | Environment.PRACTICE_SLOT_ID_TO_OBJ:
            for activity_id in Environment.GAME_ID_TO_OBJ | Environment.PRACTICE_ID_TO_OBJ:
                if (slot_id, activity_id) not in Environment.PREFERENCES:
                    Environment.PREFERENCES[(slot_id, activity_id)] = 0


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
        activity_type = self.__decide_activity_type(activity_id)
        if activity_type == ActivityType.GAME:
            return self.__parse_game_id(activity_id)
        elif activity_type == ActivityType.PRACTICE:
            return self.__parse_practice_id(activity_id)
        else:
            raise Exception("invalid activity type")


    def __parse_game_id(self, game_id: str) -> Game:
        # Parsing (splitting) game identifier (should be four resulting strings)
        split_id = game_id.split(' ')
        if len(split_id) != 4: raise RuntimeError("Issue parsing game '" + game_id + "': split does not result in four elements")
        id = game_id
        association = split_id[0]

        # Parsing age and tier
        age_tier = split_id[1].split('T')
        age = age_tier[0]
        if len(age_tier) == 2: tier = 'T' + age_tier[1]
        else: tier = None
        division = int(split_id[3])

        return Game(id, association, age, tier, division)


    def __parse_practice_id(self, practice_id: str) -> Practice:
        # return Practice("id", 0, "assoc", 0, "tier", "prac")
        pass


    def __parse_activity_slot(self, activity_slot_name: str) -> ActivitySlot:
        pass


    def __parse_game_slot(self, game_slot_name: str) -> GameSlot:
        split_line = re.split(self.COMMA_REGEX, game_slot_name)
        weekday_name = split_line[0]
        weekday = EnumValueToObjMaps.WEEKDAYS[weekday_name]
        start_time = split_line[1]
        gamemax = int(split_line[2])
        gamemin = int(split_line[3])
        is_evening_slot = self.__decide_if_evening_slot(start_time)

        return GameSlot(weekday, start_time, gamemax, gamemin, is_evening_slot)


    def __parse_practice_slot(self, practice_slot_name: str) -> PracticeSlot:
        pass

    
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
