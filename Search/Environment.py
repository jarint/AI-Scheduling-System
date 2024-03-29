'''
This class represents the environment which will store things like user input and search parameters.
'''

import logging
import pprint
from contextlib import redirect_stdout

from Enumerations import ActivityType, Weekday
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.GameSlot import GameSlot
from ScheduleObjects.PracticeSlot import PracticeSlot

class Environment:
    leaves_encountered = 0

    # <pre-parser initialization>

    SPECIAL_BOOKINGS = {
        "CMSA U12T1S": (ActivityType.PRACTICE, Weekday.TU, "18:00"), 
        "CMSA U13T1S": (ActivityType.PRACTICE, Weekday.TU, "18:00")
    }

    SLOT_ID_TO_OBJ = {} # maps slot id's to objects
    PRACTICE_SLOT_ID_TO_OBJ = {} # maps practice slot id's to practice slot instances
    GAME_SLOT_ID_TO_OBJ = {}  # maps game slot id's to game slot instances

    # </pre-parser initialization>

    # <during-parser initialization>

        # <penalty values>

    W_MINFILLED = 0
    W_PREF = 0
    W_PAIR = 0
    W_SECDIFF = 0
    PEN_GAMEMIN = 0
    PEN_PRACTICEMIN = 0
    PEN_NOTPAIRED = 0
    PEN_SECTION = 0

        # </penalty values >

    NAME = ""
    ACTIVITY_ID_TO_OBJ = {} # maps activity id's to activity instances
    GAME_ID_TO_OBJ = {} # maps game id's to instances of Game class
    PRACTICE_ID_TO_OBJ = {} # maps practice id's to instances of Practice class
    NOT_COMPATIBLE = {} # maps activity id's to lists of activity id's. Rather than storing pairs, 
        # we can store the set of all incompatible activities for some given activity
    UNWANTED = {} # lists of games/pracices that cannot be assigned to certain slots.
        # stored as a set of tuples, whose first element is an activity id, and second element is a slot id
    PREFERENCES = {} # maps activity id -> to set of tuples (slot_id, preference value)
    PAIR = {} # Games to be scheduled at the same time
        # maps activity id to a set of activity id's
    PARTASSIGN = {} # Hard Constraint. To be scheduled immediately. Maps activity id to slot id

    # </during-parser initialization>

    # <post-parser initialization>

    ACTIVITY_IDS = set()
    GAME_IDS = set()
    PRACTICE_IDS = set()
    ALL_SLOT_IDS = set()
    PRACTICE_SLOT_IDS = set()
    GAME_SLOT_IDS = set()

    MO_G_SLOTS_IDS = set()
    TU_G_SLOT_IDS = set()
    MO_P_SLOTS_IDS = set()
    TU_P_SLOT_IDS = set()
    FR_P_SLOT_IDS = set()

    
    def display_parsed_data():
        print("Game IDs: " + str(Environment.GAME_IDS))
        print("Practice IDs: " + str(Environment.PRACTICE_IDS))
        print()
        print("\nNot compatible: " + str(Environment.NOT_COMPATIBLE))
        print("\nUnwanted: " + str(Environment.UNWANTED))
        print("\nPreferences: " + str(Environment.NOT_COMPATIBLE))
        print("\nPair: " + str(Environment.PAIR))
        print("\nPartial assignments: " + str(Environment.PARTASSIGN))

    
    # to iterate over the game or practice slots on a given day
        # for slot_id in MO_G_SLOTS:
        #     slot = GAME_SLOT_ID_TO_OBJ[slot_id]
    # key: (<activity_type>, <weekday>, <start time>)


    @staticmethod
    def pre_parser_initialization():

        MO_GAME_SLOT_SHORTCUTS = [
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", 
            "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00", 
            "18:00-19:00", "19:00-20:00", "20:00-21:00"
        ]
        TU_GAME_SLOT_SHORTCUTS = [
            "8:00-9:30", "9:30-11:00", "11:00-12:30", "12:30-14:00", "14:00-15:30", 
            "15:30-17:00", "17:00-18:30", "18:30-20:00"
        ]
        MO_PRACTICE_SLOT_SHORTCUTS = [
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", 
            "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00", 
            "18:00-19:00", "19:00-20:00", "20:00-21:00"
        ]
        TU_PRACTICE_SLOT_SHORTCUTS = [
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", 
            "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00", 
            "18:00-19:00", "19:00-20:00", "20:00-21:00"
        ]
        FR_PRACTICE_SLOT_SHORTCUTS = [
            "8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", 
            "18:00-20:00"
        ]


        def time_str_to_int(time_str: str) -> int:
            try:
                hours, mins = (int(e) for e in time_str.strip().split(":"))
            except ValueError:
                raise ValueError(f"invalid time string: {time_str}")
            
            return hours * 60 + mins


        def decide_if_evening_slot(time_str: str) -> bool:
            time_int = time_str_to_int(time_str)
            return time_int >= 1080 # 18:00 - 18 * 60 = 1080


        def params(shortcut: str):
            start_time, end_time = shortcut.split("-")
            is_evening_slot = decide_if_evening_slot(start_time)
            return (start_time, end_time, is_evening_slot, 0, 0)

        MO_GAME_SLOTS = [GameSlot(Weekday.MO, *params(shortcut)) for shortcut in MO_GAME_SLOT_SHORTCUTS]
        TU_GAME_SLOTS = [GameSlot(Weekday.TU, *params(shortcut)) for shortcut in TU_GAME_SLOT_SHORTCUTS]
        MO_PRACTICE_SLOTS = [PracticeSlot(Weekday.MO, *params(shortcut)) for shortcut in MO_PRACTICE_SLOT_SHORTCUTS]
        TU_PRACTICE_SLOTS = [PracticeSlot(Weekday.TU, *params(shortcut)) for shortcut in TU_PRACTICE_SLOT_SHORTCUTS]
        FR_PRACTICE_SLOTS = [PracticeSlot(Weekday.FR, *params(shortcut)) for shortcut in FR_PRACTICE_SLOT_SHORTCUTS]

        ACTIVITY_SLOTS = MO_GAME_SLOTS + TU_GAME_SLOTS + MO_PRACTICE_SLOTS + TU_PRACTICE_SLOTS + FR_PRACTICE_SLOTS
        Environment.SLOT_ID_TO_OBJ = {slot.id: slot for slot in ACTIVITY_SLOTS}

        Environment.GAME_SLOT_ID_TO_OBJ = {slot_id: Environment.SLOT_ID_TO_OBJ[slot_id] for slot_id in
            filter(lambda id: id[0] == ActivityType.GAME, Environment.SLOT_ID_TO_OBJ)
        }  

        Environment.PRACTICE_SLOT_ID_TO_OBJ = {slot_id: Environment.SLOT_ID_TO_OBJ[slot_id] for slot_id in
            filter(lambda id: id[0] == ActivityType.PRACTICE, Environment.SLOT_ID_TO_OBJ)
        }

        Environment.ALL_SLOT_IDS = {slot_id for slot_id in Environment.SLOT_ID_TO_OBJ}
        Environment.PRACTICE_SLOT_IDS = {slot_id for slot_id in Environment.PRACTICE_SLOT_ID_TO_OBJ}
        Environment.GAME_SLOT_IDS = {slot_id for slot_id in Environment.GAME_SLOT_ID_TO_OBJ}

        Environment.MO_G_SLOTS_IDS = {slot_id for slot_id in 
            filter(lambda id: id[0] == ActivityType.GAME 
            and id[1] == Weekday.MO, Environment.ALL_SLOT_IDS)
        }
        Environment.TU_G_SLOT_IDS = {slot_id for slot_id in 
            filter(lambda id: id[0] == ActivityType.GAME 
            and id[1] == Weekday.TU, Environment.ALL_SLOT_IDS)
        }
        Environment.MO_P_SLOTS_IDS = {slot_id for slot_id in 
            filter(lambda id: id[0] == ActivityType.PRACTICE 
            and id[1] == Weekday.MO, Environment.ALL_SLOT_IDS)
        }
        Environment.TU_P_SLOT_IDS = {slot_id for slot_id in 
            filter(lambda id: id[0] == ActivityType.PRACTICE
            and id[1] == Weekday.TU, Environment.ALL_SLOT_IDS)
        }
        Environment.FR_P_SLOT_IDS = {slot_id for slot_id in 
            filter(lambda id: id[0] == ActivityType.PRACTICE 
            and id[1] == Weekday.FR, Environment.ALL_SLOT_IDS)
        }

        # <overlaps>

        for slot_a_id in Environment.ALL_SLOT_IDS:
            slot_a_obj = Environment.SLOT_ID_TO_OBJ[slot_a_id]
            slot_a_start = time_str_to_int(slot_a_obj.start_time)
            slot_a_end = time_str_to_int(slot_a_obj.end_time)
            for slot_b_id in Environment.ALL_SLOT_IDS:
                slot_b_obj = Environment.SLOT_ID_TO_OBJ[slot_b_id]
                slot_b_start = time_str_to_int(slot_b_obj.start_time)
                slot_b_end = time_str_to_int(slot_b_obj.end_time)
                if (
                    slot_a_obj.weekday == slot_b_obj.weekday
                    and not (slot_a_start >= slot_b_end or slot_a_end <= slot_b_start)
                ):
                    slot_a_obj.overlaps.add(slot_b_id)
                    slot_b_obj.overlaps.add(slot_a_id)

        # </overlaps>

    @staticmethod
    def post_parser_initialization():

        # NOTE these are for the admin meeting hard constraint
        slot_a_id = (ActivityType.GAME, Weekday.TU, "11:00")
        slot_b_id = (ActivityType.PRACTICE, Weekday.TU, "11:00")
        slot_c_id = (ActivityType.PRACTICE, Weekday.TU, "12:00")
        slot_a = Environment.SLOT_ID_TO_OBJ[slot_a_id]
        slot_b = Environment.SLOT_ID_TO_OBJ[slot_b_id]
        slot_c = Environment.SLOT_ID_TO_OBJ[slot_c_id]
        slot_a.gamemin = 0
        slot_a.gamemax = 0
        slot_b.gamemin = 0
        slot_b.gamemax = 0
        slot_c.gamemin = 0
        slot_c.gamemax = 0


        logging.debug("\n" * 5)
        logging.debug("<environment data>")
        with open('program_log.log', 'a') as f:
            with redirect_stdout(f):
                pprint.pprint(vars(Environment))
        logging.debug("</environment data>")
        logging.debug("\n" * 5)



    class Adders:

        @staticmethod
        def update_name(name: str):
            Environment.NAME = name

        # NOTE these slot adders are no longer needed because all creation of slots happens in Environment.pre_parser_initialization()
            # for this reason there is no longer a parse_practice_slot or parse_game_slot method, which simply returned instances of slots.
            # there are still parse_game_slot(s) and parse_practice_slot(s) methods, whose only purposes are to update gamemax, gamemin, practicemax, practicemin

        # @staticmethod
        # def add_game_slot(game_slot: GameSlot):
        #     Environment.GAME_SLOT_ID_TO_OBJ[game_slot.id] = game_slot
        #     Environment.GAME_SLOT_IDS.add(game_slot.id)
        

        # @staticmethod
        # def add_practice_slot(practice_slot: PracticeSlot):
        #     Environment.PRACTICE_SLOT_ID_TO_OBJ[practice_slot.id] = practice_slot
        #     Environment.PRACTICE_SLOT_IDS.add(practice_slot)
        

        @staticmethod
        def add_game(game: Game):
            Environment.ACTIVITY_ID_TO_OBJ[game.id] = game
            Environment.ACTIVITY_IDS.add(game.id)
            Environment.GAME_ID_TO_OBJ[game.id] = game
            Environment.GAME_IDS.add(game.id)
            Environment.NOT_COMPATIBLE[game.id] = set()


        @staticmethod
        def add_practice(practice: Practice):
            Environment.ACTIVITY_ID_TO_OBJ[practice.id] = practice
            Environment.ACTIVITY_IDS.add(practice.id)
            Environment.PRACTICE_ID_TO_OBJ[practice.id] = practice
            Environment.PRACTICE_IDS.add(practice.id)
            Environment.NOT_COMPATIBLE[practice.id] = set()


        @staticmethod
        def add_not_compatible(activity1_id: str, activity2_id: str):                
            Environment.NOT_COMPATIBLE[activity1_id].add(activity2_id)
            Environment.NOT_COMPATIBLE[activity2_id].add(activity1_id)


        @staticmethod
        def add_unwanted(activity_id: str, slot_id: "tuple[ActivityType, Weekday, str]"):
            if activity_id not in Environment.UNWANTED:
                Environment.UNWANTED[activity_id] = set()
            Environment.UNWANTED[activity_id].add(slot_id)


        @staticmethod
        def add_preference(preference: "tuple[str, tuple[ActivityType, Weekday, str], int]"):
            activity_id, slot_id, pref_value = preference
            Environment.PREFERENCES[activity_id].add((slot_id, pref_value))


        @staticmethod
        def add_pair(pair: "tuple[str, str]"):
            activity_a, activity_b = pair
            Environment.PAIR[activity_a].add(activity_b)
            Environment.PAIR[activity_b].add(activity_a)
        

        @staticmethod
        def add_partassign(partassign: "tuple[str, tuple[ActivityType, Weekday, str]]"):
            activity_id, slot_id = partassign
            Environment.PARTASSIGN[activity_id] = slot_id
        

        