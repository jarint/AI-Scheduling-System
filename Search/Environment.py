'''
This class represents the environment which will store things like user input and search parameters.
'''

from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.Slot import Slot

class Environment:

    # Environment data variables
    name = ''
    GAMES = [] # All game objects loaded by the parser are stored here
    PRACTICES = [] # All Practice objects loaded by the parser are stored here
    GAMESLOTS = [] # Possible Game slots stored here
    PRACTICESLOTS = [] # Possible Practice slots stored here
    NOTCOMPATIBLE = [] # needs to be stored as tuples
    UNWANTED = [] # Hard Constraint, games/pracices that cannot be assigned to certain slots
    PREFERENCES = [] # accepts a list of league preferences for time slots of games and practices - Used by soft constraint class
    PAIR = [] # Games to be scheduled at the same time - format should be tuples
    PARTASSIGN = [] # Hard Constraint. To be scheduled immediately.

    class Adders:
        @staticmethod
        def updateName(name: str):
            Environment.name = name

        @staticmethod
        def addGameSlot():
            pass
        
        @staticmethod
        def addPracticeSlot():
            pass
        
        @staticmethod
        def addGame():
            pass

        @staticmethod
        def addPractice():
            pass

        @staticmethod
        def addNotCompatible():
            pass

        @staticmethod
        def addUnwanted():
            pass

        @staticmethod
        def addPreference():
            pass

        @staticmethod
        def addPair():
            pass
        
        @staticmethod
        def addPartAssign():
            pass