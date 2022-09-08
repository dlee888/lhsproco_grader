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
        return await asyncio.wait_for(run2(cmd), timeout=time_limit)
    except asyncio.TimeoutError:
        return None


async def grade_case(program_dir, input_file, output_file, lang):
    if lang == 'C++' or lang == 'C':
        return await time(f'./{program_dir}/main < {input_file} > {output_file}', constants.TIME_LIMITS[lang])
    elif lang == 'Python':
        return await time(f'python {program_dir}/main.py < {input_file} > {output_file}', constants.TIME_LIMITS[lang])
    elif lang == 'Java':
        return await time(f'java -cp {program_dir} Main < {input_file} > {output_file}', constants.TIME_LIMITS[lang])


async def grade_problem(problem_id, lang, request_id):
    problem = problems.problem_list[problem_id]
    program = f'request_{request_id}'
    program_dir = os.path.join(constants.TEMP_DIR, program)
    sol_file = os.path.join(
        program_dir, constants.LANG_FILENAMES[lang])
    sol_without_ext = os.path.join(
        program_dir, constants.LANG_FILENAMES[lang].split('.')[0])

    if lang == 'C++':
        comp, stdout, stderr = await run2(f'g++ {sol_file} -o {sol_without_ext} -O2')
        # print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return [f'Compile error: {stderr}'], 0
    elif lang == 'C':
        comp, stdout, stderr = await run2(f'gcc {sol_file} -o {sol_without_ext} -O2')
        # print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return [f'Compile error: {stderr}'], 0
    elif lang == 'Java':
        comp, stdout, stderr = await run2(f'javac {sol_file} -d {program_dir}')
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
            program_dir, f'output_{request_id}_{i + 1}.out')

        code, stdout, stderr = await grade_case(program_dir, input_file, output_file, lang)

        if code == None:
            result.append('Time Limit Exceeded')
        elif code != 0:
            # print(code, stdout, stderr)
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
