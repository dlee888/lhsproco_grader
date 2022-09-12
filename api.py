import fastapi
import typing
import os
import time

import grading
import constants
import problems

app = fastapi.FastAPI()


def setup():
    problems.load_all()
    for path in constants.ALL_DIRS:
        os.makedirs(path, exist_ok=True)


@app.post('/grading/{event_id}/{problem_id}')
async def grade(request: fastapi.Request, event_id: str, problem_id: int, lang: str = fastapi.Form(...), file: typing.Optional[fastapi.UploadFile] = fastapi.File(...)):
    if lang not in constants.SUPPORTED_LANGS:
        return {'error': 'Unsupported language'}
    if event_id not in problems.events_list.keys():
        return {'error': 'Invalid event id'}
    if problem_id not in problems.events_list[event_id].problems.keys():
        return {'error': 'Invalid problem id'}
    if file is None:
        return {'error': 'No file uploaded'}
    # Save file to disk
    program = f'submission_{request.client.host}_{round(time.time() * 100)}'
    program_dir = os.path.join(constants.TEMP_DIR, program)
    os.makedirs(program_dir, exist_ok=True)
    with open(os.path.join(constants.TEMP_DIR, program, constants.LANG_FILENAMES[lang]), 'wb') as f:
        f.write(await file.read())
    # Run grading
    result = await grading.grade_problem(program, event_id, problem_id, lang)
    return result


setup()
