import os

import constants


class Problem:

    def __init__(self, event_id, problem_number, test_cases):
        self.event_id = event_id
        self.problem_number = problem_number
        self.test_cases = test_cases

    def testcase_dir(self):
        return os.path.join(constants.PROBLEMS_DIR, os.path.join(str(self.event_id), str(self.problem_number)))

    def input_file(self, testcase_number):
        return os.path.join(self.testcase_dir(), f'{testcase_number + 1}.in')

    def output_file(self, testcase_number):
        return os.path.join(self.testcase_dir(), f'{testcase_number + 1}.out')


class Event:
    def __init__(self, event_id, problems):
        self.id = event_id
        self.problems = problems

    def get_problem(self, problem_number):
        return self.problems[problem_number]


events_list = {}


def load_problem(event, problem):
    return Problem(event, problem, len(os.listdir(os.path.join(constants.PROBLEMS_DIR, os.path.join(event, problem)))) // 2)


def load_event(dir):
    problems = {}
    for problem in os.listdir(os.path.join(constants.PROBLEMS_DIR, dir)):
        problems[int(problem)] = load_problem(dir, problem)
    return Event(dir, problems)


def load_all():
    global events_list
    events_list = {}
    for event in os.listdir(constants.PROBLEMS_DIR):
        events_list[event] = load_event(event)
