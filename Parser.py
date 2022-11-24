'''
This class parses the input files for the decision problem and loads the information therein to data structures and objects
that can be used by the AI to generate a schedule.

'''

import sys
import logging
import os
import re

from Search.Environment import Environment
from Enumerations import ActivityType


def parse(env: Environment):
    Parser(env)


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


    def __init__(self, env: Environment) -> None:
        self.env = env
        self.__parse_commandline_args()
        self.__parse_file()


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
            self.env.w_minfilled,
            self.env.w_pref,
            self.env.w_pair,
            self.env.w_secdiff,
            self.env.pen_gamemin, 
            self.env.pen_practicemin, 
            self.env.pen_notpaired, 
            self.env.pen_section
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

            split_line = re.split(self.COMMA_REGEX, line)
            day = split_line[0]
            start_time = split_line[1]
            gamemax = int(split_line[2])
            gamemin = int(split_line[3])
            # self.env.Adders.add_game_slot(day, start_time, gamemax, gamemin)


    def __parse_practice_slots(self) -> None:
        logging.debug("  __parse_practice_slots")
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_games(self) -> None:
        logging.debug("  __parse_games")
        while (self.__next_line() is not None):
            # This is the game identifier
            line = self.line_str

            # Parsing (splitting) game identifier (should be four resulting strings)
            split_line = line.split(' ')
            if len(split_line) != 4: raise RuntimeError("Issue parsing game '" + line + "': split does not result in four elements")

            id = line
            association = split_line[0]
            division = int(split_line[3])

            # Parsing age and tier
            age_tier = split_line[1].split('T')
            age = age_tier[0]
            if len(age_tier) == 2: tier = 'T' + age_tier[1]
            else: tier = None

            # Adding game to environment
            self.env.Adders.add_game(id, association, age, tier, division)


    def __parse_practices(self) -> None:
        logging.debug("  __parse_practices")
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_not_compatible(self) -> None:
        logging.debug("  __parse_not_compatible")
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_unwanted(self) -> None:
        logging.debug("  __parse_unwanted")
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_preferences(self) -> None:
        logging.debug("  __parse_preferences")
        while (self.__next_line() is not None):
            line = self.line_str
            split_line = line.split(self.COMMA_REGEX)


    def __parse_pairs(self) -> None:
        logging.debug("  __parse_pairs")
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_partial_assignments(self) -> None:
        logging.debug("  __parse_partial_assignments")
        while (self.__next_line() is not None):
            line = self.line_str


    # </file parsing methods>


    def __parse_activity_id(self, activity_id: str) -> None:
        activity_type = self.__decide_activity_type(activity_id)
        if activity_type == ActivityType.GAME:
            pass
        elif activity_type == ActivityType.PRACTICE:
            pass
        else:
            pass

    
    def __decide_activity_type(self, activity_id: str) -> str:
        # TODO
        return ActivityType.GAME
    

    
    