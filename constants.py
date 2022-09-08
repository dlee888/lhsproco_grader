import os

DATA_DIR = 'data'

ASSETS_DIR = os.path.join(DATA_DIR, 'assets')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')

TCASE_DIR = os.path.join(ASSETS_DIR, 'test_data')
PROBLEMS_DIR = os.path.join(ASSETS_DIR, 'problems')

ALL_DIRS = (attrib_value for attrib_name, attrib_value in list(globals().items())
            if attrib_name.endswith('DIR'))

SUPPORTED_LANGS = ['C++', 'Python', 'C']
LANG_EXTENSIONS = {
    'C++': '.cpp',
    'Python': '.py',
    'C': '.c'
}