
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
            if game_id in Environment.SPECIAL_BOOKINGS:
                assignment = (game_id, Environment.SPECIAL_BOOKINGS[game_id])
                if HardConstraints.check_constraints(schedule, assignment):
                    assignments.append(assignment)
            else:
                for game_slot_id in schedule.vacant_game_slots:
                    assignment = (game_id, game_slot_id)
                    if HardConstraints.check_constraints(schedule, assignment):
                        assignments.append(assignment)

        # Generating possible assignments for practices
        for practice_id in schedule.remaining_practices:
            for practice_slot_id in schedule.vacant_practice_slots:
                assignment = (practice_id, practice_slot_id)
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
            new_schedule = schedule.get_copy()
            activity_id, slot_id = assign
            new_schedule.eval = new_schedule.eval + SoftConstraints.get_delta_eval(new_schedule, assign)
            new_schedule.assign_activity(activity_id, slot_id)
            new_schedule.latest_assignment = assign
            schedules.append(new_schedule)

        return schedules