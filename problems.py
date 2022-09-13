import os
from typing import *

import constants


class Problem:

    def __init__(self, event_id: str, problem_number: int, test_cases: int) -> None:
        self.event_id = event_id
        self.problem_number = problem_number
        self.test_cases = test_cases

    def testcase_dir(self) -> str:
        '''Returns the directory where the test cases are stored'''
        return os.path.join(constants.PROBLEMS_DIR, os.path.join(str(self.event_id), str(self.problem_number)))

    def input_file(self, testcase_number: int) -> str:
        '''Returns the path to the input file for the given testcase'''
        return os.path.join(self.testcase_dir(), f'{testcase_number + 1}.in')

    def output_file(self, testcase_number: int) -> str:
        '''Returns the path to the output file for the given testcase'''
        return os.path.join(self.testcase_dir(), f'{testcase_number + 1}.out')


class Event:
    def __init__(self, event_id: str, problems: Dict[int, Problem]) -> None:
        self.id = event_id
        self.problems = problems

    def get_problem(self, problem_number: int) -> Problem:
        '''Returns the problem with the given problem number'''
        return self.problems[problem_number]


events_list = {}


def load_problem(event: str, problem: str):
    '''Loads the problem in a given directory'''
    return Problem(event, problem, len(os.listdir(os.path.join(constants.PROBLEMS_DIR, os.path.join(event, problem)))) // 2)


def load_event(dir: str):
    '''Loads the event in a given directory and loads all of its problems'''
    problems = {}
    for problem in os.listdir(os.path.join(constants.PROBLEMS_DIR, dir)):
        problems[int(problem)] = load_problem(dir, problem)
    return Event(dir, problems)


def load_all():
    '''Loads all events and problems'''
    global events_list
    events_list = {}
    for event in os.listdir(constants.PROBLEMS_DIR):
        events_list[event] = load_event(event)
