'''
This class parses the input files for the decision problem and loads the information therein to data structures and objects
that can be used by the AI to generate a schedule.

'''

import sys

from Search.Environment import Environment

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
        self.line_str = next_line  
        return next_line
        

    
    def parse_id(self, id: str):
        pass

        
    def __parse_commandline_args(self) -> None:
        args = sys.argv
        self.filename = args[0]
        (
            self.env.w_minfilled,
            self.env.w_pref,
            self.env.w_pair,
            self.env.w_secdiff,
            self.env.pen_gamemin, 
            self.env.pen_practicemin, 
            self.env.pen_notpaired, 
            self.env.pen_section
        ) = (int(arg) for arg in args[1:])


    def __parse_file(self) -> None:
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
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_game_slots(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_practice_slots(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_games(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_practices(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_not_compatible(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_unwanted(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_preferences(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_pairs(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str


    def __parse_partial_assignments(self) -> None:
        while (self.__next_line() is not None):
            line = self.line_str
    

    
    