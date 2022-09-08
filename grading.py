import asyncio
import os

import constants
import problems


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    # print(f'Done running {cmd}\n{stdout}\n{stderr}')

    return proc.returncode


async def run2(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return proc.returncode, stdout, stderr


async def time(cmd, time_limit):
    # print('Timing', cmd)
    try:
        return await asyncio.wait_for(run(cmd), timeout=time_limit)
    except asyncio.TimeoutError:
        return None


async def grade_case(program, input_file, output_file, lang):
    sol_file = os.path.join(
        constants.TEMP_DIR, f'{program}{constants.LANG_EXTENSIONS[lang]}')
    sol_without_ext = os.path.join(constants.TEMP_DIR, program)

    if lang == 'C++' or lang == 'C':
        return await time(f'./{sol_without_ext} < {input_file} > {output_file}', 2)
    elif lang == 'Python':
        return await time(f'python {sol_file} < {input_file} > {output_file}', 2)


async def grade_problem(problem_id, lang, request_id):
    problem = problems.problem_list[problem_id]
    program = f'request_{request_id}'
    sol_file = os.path.join(
        constants.TEMP_DIR, f'{program}{constants.LANG_EXTENSIONS[lang]}')
    sol_without_ext = os.path.join(constants.TEMP_DIR, program)

    if lang == 'C++':
        comp, stdout, stderr = await run2(f'g++ {sol_file} -o {sol_without_ext} -O2')
        # print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return [f'Compile error: {stderr}'], 0
    if lang == 'C':
        comp, stdout, stderr = await run2(f'gcc {sol_file} -o {sol_without_ext} -O2')
        # print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return [f'Compile error: {stderr}'], 0

    result = []
    marks = 0
    for i in range(problem.test_cases):
        input_file = os.path.join(
            problems.problem_list[problem_id].testcase_dir, f'{i + 1}.in')
        answer_file = os.path.join(
            problems.problem_list[problem_id].testcase_dir, f'{i + 1}.out')
        output_file = os.path.join(
            constants.TEMP_DIR, f'output_{request_id}_{i + 1}.out')

        code = await grade_case(program, input_file, output_file, lang)

        if code == None:
            result.append('Time Limit Exceeded')
        elif code == 1:
            result.append('Runtime error')
        else:
            diff = await run(f'diff -w {answer_file} {output_file}')
            if diff != 0:
                result.append('Wrong answer')
            else:
                result.append('Correct')
                marks += 1

    return result, marks / problem.test_cases


def detect_lang(filename):
    for lang in constants.SUPPORTED_LANGS:
        if filename.endswith(constants.LANG_EXTENSIONS[lang]):
            return lang
