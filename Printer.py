#   This class prints out the generated schedule at the end of our search process.

from Scheduler import Scheduler
from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.GameSlot import GameSlot
from ScheduleObjects.PracticeSlot import PracticeSlot
from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType
from Search.Environment import Environment




class Printer():

    #Constructor
    def __init__(self) -> None:
        pass

    def printSchedule(schedule: Schedule):
        #schedule = schedule.get_copy() <- not sure if need this
        print("Eval-value: " + str(schedule.getEval()))
        for activity in schedule.slot_of_each_activity:
            if (Environment.ACTIVITY_ID_TO_OBJ[activity].ACTIVITY_TYPE == ActivityType.GAME):
                print(
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].association) + " " +
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].age) +
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].tier) + 
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].division) + "          :" +
                    str(Environment.GAME_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].weekday) + "," +
                    str(Environment.GAME_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].start_time)
                )
            elif (Environment.ACTIVITY_ID_TO_OBJ[activity].ACTIVITY_TYPE == ActivityType.PRACTICE):
                print(
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].association) + " " +
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].age) +
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].tier) + 
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].division) + 
                    str(Environment.ACTIVITY_ID_TO_OBJ[activity].practice_num) + "          :" +
                    str(Environment.PRACTICE_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].weekday) + "," +
                    str(Environment.PRACTICE_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].start_time)
                )
        