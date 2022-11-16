## Functional Requirements



## Software layout

class: InputParameters
- description: singleton instance stores all parsed input data and command-line arguments in appropriate data structures
- constructor: invokes commandline_args() and parse_file()
- private method: commandline_args() - pareses command line arguments
- private method: parse_file(file) - parses file

class: Env
- stores the command line arguments for penalties


class: Schedule
- var: mon_game_slots
- var: tues_game_slots
- var: mon_practice_slots 
- var: tues_practice_slots
- var: fri_practice_slots
    - each of the above 5 variables is a hashmap from slot id to a set of game id's or practice id's, depending on the slot type. (each slot is an instance of the Slot class)

- var: game_assigned ? - hashmap from game id to slot
- var: practice_assigned ? - hashmap from practice id to slot

- currently_assigned(activity) - returns which slot a given activity is assigned to. This will be equal to $ if it isn't assigned anywhere.


abstract class: Activity
- superclass of Game and Practice classes


class: Game (subclass of Activity)
- var: id 
- var: division


class: Practice (subclass of Activity)
- var: id 
- var: division
- var: team


class: Slot
- var: id


class: SearchProcess ?


class: SearchModel ?


class: Div ?


class: Prob ?


class: HardConstraints
- private var: incompatible - hashmap of sets
    - maps game or practice id to a set of id's of games or practices that are not compatible with it.

- method: get_incompatible(activity)
    - returns a set of ids of activities (games/practices) incompatible with the given activity by referencing the not_compatible variable.

- int method: gamemax(slot)
- int method: practicemax(slot)

- bool method: sat_all_hard_constraints(schedule)
- bool method: sat_different_times_games_practices(schedule)
    - requires a table of not_compatible
- bool method: sat_partassign(schedule)
    - determines whether partassign is satisfied
- bool method: sat_unwanted(schedule)

- bool method: sat_city_of_calgary(schedule)
    - determines whether all city of calgary constraints are met (calls a  subroutine for each)


class: SoftConstraints
- private var: all_pairs - list of pairs of activities that are preferred at the same time
- private var: paired - hashmap from activity id to set of activity id's, representing the set of all activities that the given activity is preferred to be paired with.

- method: get_paired(activity) - references "paired" variable and returns a set of preferred games paired to that game.

- int method: gamemin(slot)
- int method: practicemin(slot)
- int method: preference(activity, slot)

- int method: eval(schedule)


