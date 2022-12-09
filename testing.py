from ScheduleObjects.Game import Game
from ScheduleObjects.Practice import Practice
from Search.Environment import Environment

games_and_practices_string = "CMSA U13T3 DIV 01 PRC 01, CMSA U13T3 DIV 02 OPN 02"
activity_1, activity_2 = games_and_practices_string.split(', ')
Environment.NOT_COMPATIBLE[activity_1].append(activity_2)
Environment.NOT_COMPATIBLE[activity_2].append(activity_1)


unwanted_schedule_string = "CMSA U13T3 DIV 01, MO, 8:00"
