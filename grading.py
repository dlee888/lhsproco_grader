import asyncio
import os
import resource
import signal
import time

import constants
import problems


def limit_virtual_memory():
    '''Limit virtual memory to 256 MB'''
    resource.setrlimit(resource.RLIMIT_AS,
                       (constants.MEMORY_LIMIT, constants.MEMORY_LIMIT))


async def run(cmd: str, **kwargs):
    '''Run a command and return the return code, stdout, and stderr'''
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE, **kwargs)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return proc.returncode, stdout, stderr


async def time_cmd(cmd: str, time_limit: float, **kwargs):
    '''
    Run a command and return the return code, stdout, stderr, and time taken
    If the command takes longer than time_limit, it will stop the command
    '''
    # print('Timing', cmd)
    try:
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE, start_new_session=True, **kwargs)

        starttime = time.time()
        stdout, stderr = await asyncio.wait_for(proc.communicate(), time_limit)
        total_time = time.time() - starttime
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        return proc.returncode, stdout, stderr, total_time
    except asyncio.TimeoutError:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        return None, None, None, time_limit


async def grade_case(program_dir: str, input_file: str, output_file: str, lang: str):
    '''Grade a single test case'''
    if lang == 'C++' or lang == 'C':
        return await time_cmd(f'./{program_dir}/main < {input_file} > {output_file}', constants.TIME_LIMITS[lang], preexec_fn=limit_virtual_memory)
    elif lang == 'Python':
        return await time_cmd(f'python {program_dir}/main.py < {input_file} > {output_file}', constants.TIME_LIMITS[lang], preexec_fn=limit_virtual_memory)
    elif lang == 'Java':
        return await time_cmd(f'java -Xmx{constants.MEMORY_LIMIT} -cp {program_dir} Main < {input_file} > {output_file}', constants.TIME_LIMITS[lang])
    else:
        raise Exception('Unsupported language')


async def grade_problem(program: str, event_id: str, problem_id: int, lang: str):
    '''Grades all test cases for a problem. Returns a list of the results for each case'''
	# TODO: prevent hacking
    problem = problems.events_list[event_id].get_problem(problem_id)
    program_dir = os.path.join(constants.TEMP_DIR, program)
    sol_file = os.path.join(
        program_dir, constants.LANG_FILENAMES[lang])
    sol_without_ext = os.path.join(
        program_dir, constants.LANG_FILENAMES[lang].split('.')[0])

    if lang == 'C++':
        comp, stdout, stderr = await run(f'g++ {sol_file} -o {sol_without_ext} -O2 -lm -std=c++17')
        # print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return {'result': 'Compile error', 'stderr': stderr}, 0
    elif lang == 'C':
        comp, stdout, stderr = await run(f'gcc {sol_file} -o {sol_without_ext} -O2')
        # print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return {'result': 'Compile error', 'stderr': stderr}, 0
    elif lang == 'Java':
        comp, stdout, stderr = await run(f'javac {sol_file} -d {program_dir}')
        print(f'Compile done\nstdout:\n{stdout}\nstderr:\n{stderr}\n{comp}')
        if comp != 0:
            return {'result': 'Compile error', 'stderr': stderr}, 0

    result = []
    for i in range(problem.test_cases):
        input_file = problem.input_file(i)
        answer_file = problem.output_file(i)
        output_file = os.path.join(
            program_dir, f'output_{i}.out')

        code, stdout, stderr, runtime = await grade_case(program_dir, input_file, output_file, lang)

        if code == None:
            result.append({'result': 'T', 'time': runtime})
        elif code != 0:
            print(code, stdout, stderr)
            result.append({'result': '!', 'time': runtime})
        else:
            diff, _, _ = await run(f'diff -w {answer_file} {output_file}')
            if diff != 0:
                result.append({'result': 'W', 'time': runtime})
            else:
                result.append({'result': 'C', 'time': runtime})

    return result
