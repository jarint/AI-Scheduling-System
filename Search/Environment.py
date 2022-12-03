'''
This class represents the environment which will store things like user input and search parameters.
'''

from Enumerations import ActivityType, Weekday
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.GameSlot import GameSlot
from ScheduleObjects.PracticeSlot import PracticeSlot

class Environment:

    # File input data
    NAME = ""
    GAME_ID_TO_OBJ = {} # maps game id's to instances of Game class
    PRACTICE_ID_TO_OBJ = {} # maps practice id's to instances of Practice class
    GAME_SLOT_ID_TO_OBJ = {} # maps game slot id's to game slot instances
    PRACTICE_SLOT_ID_TO_OBJ = {} # maps practice slot id's to practice slot instances
    NOT_COMPATIBLE = {} # maps activity id's to sets of activity id's. Rather than storing pairs, 
        # we can store the set of all incompatible activities for some given activity
    UNWANTED = {} # games/pracices that cannot be assigned to certain slots.
        # stored as a set of tuples, whose first element is an activity id, and second element is a slot id
    PREFERENCES = {} # maps (slot id, activity id) -> preference value
    PAIR = {} # Games to be scheduled at the same time
        # maps activity id to a set of activity id's
    PARTASSIGN = {} # Hard Constraint. To be scheduled immediately. List of 2-tuples whose first entry is an activity id
        # and whose second entry is a slot id
    
    MO_G_SLOTS = []
    TU_G_SLOT = [] 
    MO_P_SLOTS = []
    TU_P_SLOTS = []
    FR_P_SLOTS = []
    
    # to iterate over the game or practice slots on a given day
        # for slot_id in MO_G_SLOTS:
        #     slot = GAME_SLOT_ID_TO_OBJ[slot_id]
    

    @staticmethod
    def initialize():
        # intialize GAME_SLOT_ID_TO_OBJ
        # initialize PRACTICE_SLOT_ID_TO_OBJ
        # key: (<activity_type>, <weekday>, <start time>)
        pass


    class Adders:

        @staticmethod
        def update_name(name: str):
            Environment.NAME = name


        @staticmethod
        def add_game_slot(game_slot: GameSlot):
            Environment.GAME_SLOT_ID_TO_OBJ[game_slot.id] = game_slot
        

        @staticmethod
        def add_practice_slot():
            pass
        

        @staticmethod
        def add_game(game: Game):
            Environment.GAME_ID_TO_OBJ[game.id] = game


        @staticmethod
        def add_practice(practice: Practice):
            pass


        @staticmethod
        def add_not_compatible(activity1_id: str, activity2_id: str):
            if  True: pass


        @staticmethod
        def add_unwanted():
            pass


        @staticmethod
        def add_preference(preference: "tuple[tuple[ActivityType, Weekday, str], str, int]"):
            slot_id, activity_id, pref_value = preference
            Environment.PREFERENCES[slot_id, activity_id] = pref_value


        @staticmethod
        def add_pair(pair: "tuple[str, str]"):
            activity_a, activity_b = pair
            Environment.PAIR[activity_a] = Environment.PAIR[activity_a].union(Environment.PAIR[activity_b])
            Environment.PAIR[activity_b] = Environment.PAIR[activity_b].union(Environment.PAIR[activity_a])
            Environment.PAIR[activity_a].add(activity_b)
            Environment.PAIR[activity_b].add(activity_a)
        

        @staticmethod
        def add_partassign(partassign: "tuple[str, str]"):
            Environment.Adders.add_partassign(partassign)