## Software layout


main.py - driver code
- invokes parser and then search


class: Scheduler - employs the search process

class: Printer - prints schedules

class: Tree - tree where we can perform depth-first search

class: Node - a node in the tree which stores a schedule

class: Parser
- description: singleton instance stores all parsed input data and command-line arguments in appropriate data structures
- method: commandline_args() - pareses command line arguments
- method: parse_file(file) - parses file

class: Environment
- stores all data from parsed file data and commandline arguments


class: Schedule
- var: assignments - map from slot id to set of activity id's



abstract class: Activity
- superclass of Game and Practice classes


class: Game (subclass of Activity)
- var: id 
- var: division


class: Practice (subclass of Activity)
- var: id 
- var: division
- var: team


class: ActivitySlot (abstract class for GameSlot and PracticeSlot)
- var: id


class: GameSlot
- represents a game slot and has an id

class: PracticeSlot
- represents a practice slot and has an id


class: SearchModel
- method: div


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


Enumerations.py
- enumerates weekdays and activity types


