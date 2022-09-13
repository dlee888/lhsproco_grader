import fastapi
import typing
import os
import time
import shutil

import aws
import grading
import constants
import problems

app = fastapi.FastAPI()


def setup():
    aws.sync_all()
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


@app.get('/ping')
async def ping():
    return {'pong': True}


@app.post('/problems/upload/{event_id}/{problem_id}')
async def upload_problem(event_id: str, problem_id: int, file: typing.Optional[fastapi.UploadFile] = fastapi.File(...)):
    if event_id not in problems.events_list.keys():
        return {'error': 'Invalid event id'}
    if file is None:
        return {'error': 'No file uploaded'}
    # Save file to disk
    file_path = os.path.join(
        constants.TEMP_DIR, f'upload_{event_id}_{problem_id}_{round(time.time() * 100)}.zip')
    with open(file_path, 'wb') as f:
        f.write(await file.read())
    # Unzip file
    shutil.rmtree(os.path.join(constants.PROBLEMS_DIR, event_id,
                  str(problem_id)), ignore_errors=True)
    os.makedirs(os.path.join(constants.PROBLEMS_DIR,
                event_id, str(problem_id)))
    os.system(
        f'unzip {file_path} -d {os.path.join(constants.PROBLEMS_DIR, event_id, str(problem_id))}')
    aws.upload_folder(os.path.join(
        constants.PROBLEMS_DIR, event_id, str(problem_id)))
    problems.load_all()
    return {'success': True}

setup()
