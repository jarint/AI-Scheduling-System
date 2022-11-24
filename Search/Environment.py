'''
This class represents the environment which will store things like user input and search parameters.
'''

from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice

class Environment:

    # File input data
    NAME = ""
    GAME_ID_TO_OBJ = {} # maps game id's to instances of Game class
    PRACTICE_ID_TO_OBJ = {} # maps practice id's to instances of Practice class
    GAME_SLOT_ID_TO_OBJ = {} # maps game slot id's to game slot instances
    PRACTICE_SLOT_ID_TO_OBJ = {} # maps practice slot id's to practice slot instances
    NOT_COMPATIBLE = {} # maps activity id's to sets of activity id's. Rather than storing pairs, 
        # we can store the set of all incompatible activities for some given activity
    UNWANTED = set() # games/pracices that cannot be assigned to certain slots.
        # stored as a set of tuples, whose first element is an activity id, and second element is a slot id
    PREFERENCES = [] # a list of league preferences for time slots of games and practices
    PAIR = {} # Games to be scheduled at the same time
        # maps activity id to another acitivity id 
    PARTASSIGN = [] # Hard Constraint. To be scheduled immediately. List of 2-tuples whose first entry is an activity id
        # and whose second entry is a slot id

    class Adders:

        @staticmethod
        def update_name(name: str):
            Environment.name = name


        @staticmethod
        def add_game_slot(day: str, start_time: str, gamemax: int, gamemin: int):
            # Environment.GAMESLOTS.append()
            pass
        

        @staticmethod
        def add_practice_slot():
            pass
        

        @staticmethod
        def add_game(id: str, association: str, age: str, tier: str, division: int):
            Environment.GAME_ID_TO_OBJ[id] = Game(id, association, age, tier, division)


        @staticmethod
        def add_practice():
            pass


        @staticmethod
        def add_not_compatible():
            pass


        @staticmethod
        def add_unwanted():
            pass


        @staticmethod
        def add_preference():
            pass


        @staticmethod
        def add_pair():
            pass
        

        @staticmethod
        def add_partassign():
            pass