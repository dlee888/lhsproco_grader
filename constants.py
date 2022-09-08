import os

DATA_DIR = 'data'

ASSETS_DIR = os.path.join(DATA_DIR, 'assets')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')

TCASE_DIR = os.path.join(ASSETS_DIR, 'test_data')
PROBLEMS_DIR = os.path.join(ASSETS_DIR, 'problems')

ALL_DIRS = (attrib_value for attrib_name, attrib_value in list(globals().items())
            if attrib_name.endswith('DIR'))

SUPPORTED_LANGS = ['C++', 'Python', 'C', 'Java']
LANG_EXTENSIONS = {
    'C++': '.cpp',
    'Python': '.py',
    'C': '.c',
    'Java': '.java'
}
LANG_FILENAMES = {
    'C++': 'main.cpp',
    'Python': 'main.py',
    'C': 'main.c',
    'Java': 'Main.java'
}
TIME_LIMITS = {
    'C++': 2,
    'Python': 6,
    'C': 2,
    'Java': 3
}