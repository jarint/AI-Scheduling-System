
from ScheduleObjects.Schedule import Schedule
from Constraints.HardConstraints import HardConstraints
from Constraints.SoftConstraints import SoftConstraints
from Search.Environment import Environment

class SearchModel:
    @staticmethod
    def div(schedule: Schedule):
        """
        Input: A schedule to expand.
        Output: A list of all possible schedules produced by assigning a single game or practice to any available slot, where that assignment does not violate hard constraints.
        Note that we will never generate a new schedule (we only produce copies).
            Therefore, the only schedule 'initialized' is the very first empty schedule.
            In this way, the integrity of the 'remaining_games' and 'remaining_practices' variables is preserved.
            Game and practice are removed from their respective 'remaining' lists in a schedule upon being assigned to the schedule.
        """
        assignments = [] # list of tuples, where each represents an assignment

        # Generating possible assignments for games
        for game_id in schedule.remaining_games:
            for game_slot_id in Environment.GAME_SLOT_IDS:
                assignment = tuple(game_id, game_slot_id)
                if HardConstraints.check_constraints(schedule, assignment):
                    assignments.append(assignment)

        # Generating possible assignments for practices
        for practice_id in schedule.remaining_practices:
            for practice_slot_id in Environment.PRACTICE_SLOT_IDS:
                assignment = tuple(practice_id, practice_slot_id)
                if HardConstraints.check_constraints(schedule, assignment):
                    assignments.append(assignment)

        # Generating and returning new Schedule objects for each of these new assignments
        return SearchModel.generate_schedules(schedule, assignments)


    @staticmethod
    def generate_schedules(schedule: Schedule, assignments):
        """
        Input: List of assignments, where each assignment is represented by a 2-tuple containing an activity ID and a slot ID
        Output: List of Schedule objects, where each corresponds to the addition of one of the new assignments given as input
        """
        schedules = []

        for assign in assignments:
            schedule = schedule.get_copy()
            activity_id, slot_id = assign
            schedule.assign_activity(activity_id, slot_id)
            schedule.penalty = schedule.penalty + SoftConstraints.get_delta_penalty(schedule, assign)
            schedules.append(schedule)

        return schedules