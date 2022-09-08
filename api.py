import fastapi
import typing
import os

import grading
import constants
import problems

api = fastapi.FastAPI()

def setup():
	problems.load_all()
	for path in constants.ALL_DIRS:
		os.makedirs(path, exist_ok=True)


request_id = 0


@api.post('/grade/{problem_id}')
async def grade(request: fastapi.Request, problem_id: int, lang: str = fastapi.Form(...), file: typing.Optional[fastapi.UploadFile] = fastapi.File(...)):
    if lang not in constants.SUPPORTED_LANGS:
        return {'error': 'Unsupported language'}
    if problem_id >= len(problems.problem_list):
        return {'error': 'Invalid problem id'}
    if file is None:
        return {'error': 'No file uploaded'}
    global request_id
    request_id += 1
    # Save file to disk
    program = f'request_{request_id}'
    program_dir = os.path.join(constants.TEMP_DIR, program)
    os.makedirs(program_dir, exist_ok=True)
    with open(os.path.join(constants.TEMP_DIR, f'request_{request_id}', constants.LANG_FILENAMES[lang]), 'wb') as f:
        f.write(await file.read())
    # Run grading
    result, marks = await grading.grade_problem(problem_id, lang, request_id)
    return result


setup()