#   This class prints out the generated schedule at the end of our search process.

from ScheduleObjects.Schedule import Schedule
from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from ScheduleObjects.GameSlot import GameSlot
from ScheduleObjects.PracticeSlot import PracticeSlot
from ScheduleObjects.Activity import Activity
from Enumerations import ActivityType
from Enumerations import Weekday
from Search.Environment import Environment




class Printer():

    #Constructor
    def __init__(self) -> None:
        pass

    def print_schedule(schedule: Schedule):
        #schedule = schedule.get_copy() <- not sure if need this
        BUFFER_SPACE = 30

        print("Eval-value: " + str(schedule.getEval()))
        for activity_id in schedule.slot_of_each_activity:
            activity = Environment.ACTIVITY_ID_TO_OBJ[activity_id]
            slot_id = schedule.slot_of_each_activity[activity_id]
            activity_type, weekday, start_time = slot_id

            num_spaces = BUFFER_SPACE - len(activity_id) 

            print(
                activity_id + " " * num_spaces + ": " +
                weekday.value + ", " + start_time
            )


            # if (Environment.ACTIVITY_ID_TO_OBJ[activity].ACTIVITY_TYPE == ActivityType.GAME):
            #     print(
            #         str(Environment.ACTIVITY_ID_TO_OBJ[activity].id) + "          :" +
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].association) + " " +
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].age) +
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].tier) + 
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].division) + "          :" +
            #         str(Environment.GAME_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].weekday) + "," +
            #         str(Environment.GAME_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].start_time)
            #     )
            # elif (Environment.ACTIVITY_ID_TO_OBJ[activity].ACTIVITY_TYPE == ActivityType.PRACTICE):
            #     print(
            #         str(Environment.ACTIVITY_ID_TO_OBJ[activity].id) + "          :" +
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].association) + " " +
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].age) +
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].tier) + 
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].division) + 
            #         # str(Environment.ACTIVITY_ID_TO_OBJ[activity].practice_num) + "          :" +
            #         str(Environment.PRACTICE_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].weekday) + "," +
            #         str(Environment.PRACTICE_SLOT_ID_TO_OBJ[schedule.slot_of_each_activity[activity]].start_time)
            #     )
        