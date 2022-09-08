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
    global request_id
    request_id += 1
    # Save file to disk
    with open(os.path.join(constants.TEMP_DIR, f'request_{request_id}{constants.LANG_EXTENSIONS[lang]}'), 'wb') as f:
        f.write(await file.read())
    # Run grading
    result, marks = await grading.grade_problem(problem_id, lang, request_id)
    return result


setup()