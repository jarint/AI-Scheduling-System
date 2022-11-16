'''
This class is the container for the scheduling AI. It calls the methods in order to parse an input file and returns a completed
schedule at the end of the evaluation process.

'''

from ScheduleObjects.Schedule import Schedule
from Search.Environment import Environment
from Parser import Parser


class Scheduler:

    def __init__(self) -> None:
        self.env: Environment = Environment()
        self.parser: Parser = Parser(self.env)

    
    # start function internal methods start the search process
    def search():
        # internal methods start the scheduling process
        pass
