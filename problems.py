import os

import constants

class Problem:
    
    def __init__(self, name, statement, test_cases, testcase_dir):
        self.name = name
        self.statement = statement
        self.test_cases = test_cases
        self.testcase_dir = testcase_dir
    
problem_list = []

def load_problem(dir):
    statement = open(os.path.join(constants.PROBLEMS_DIR, dir, 'statement.txt'), 'r').readlines()
    
    name = statement[0].strip()
    problem = '\n'.join(statement[1:])
    test_cases = len(os.listdir(os.path.join(constants.TCASE_DIR, dir))) // 2
    
    problem_list.append(Problem(name, problem, test_cases, os.path.join(constants.TCASE_DIR, dir)))
    
def load_all():
    for problem in os.listdir(constants.PROBLEMS_DIR):
        load_problem(problem)