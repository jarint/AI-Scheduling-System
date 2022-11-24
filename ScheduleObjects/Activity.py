'''
The superclass of all games and practices. Any shared behavior between the two classes may be placed here.
'''

from abc import ABC, abstractmethod


class Activity(ABC):

    ACTIVITY_TYPE = None

    '''
    abstract class; no constructor needed.
    '''



