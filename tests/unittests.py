import requests


def post(url, **kwargs):
    return requests.post(url, **kwargs)


def send_solution(filename, lang, url):
    with open(filename, 'r') as f:
        return post(url, data={'lang': lang}, files={'file': f})


def send_problem(filename, url):
    with open(filename, 'rb') as f:
        return post(url, files={'file': f})


tests = [
    {
        'filename': 'add.c',
        'lang': 'C',
                'expected': [
                    "C",
                    "C",
                    "C",
                ]
    },
    {
        'filename': 'add_wrong.c',
        'lang': 'C',
                'expected': [
                    "C",
                    "W",
                    "W",
                ]
    },
    {
        'filename': 'add.cpp',
        'lang': 'C++',
                'expected': [
                    "C",
                    "C",
                    "C",
                ]
    },
    {
        'filename': 'add_wrong.cpp',
        'lang': 'C++',
                'expected': [
                    "W",
                    "C",
                    "W",
                ]
    },
    {
        'filename': 'add_mle.cpp',
        'lang': 'C++',
                'expected': [
                    "!",
                    "!",
                    "!",
                ]
    },
    {
        'filename': 'add_rte.cpp',
        'lang': 'C++',
                'expected': [
                    "!",
                    "!",
                    "!",
                ]
    },
    {
        'filename': 'add_tle.cpp',
        'lang': 'C++',
                'expected': [
                    "W",
                    "W",
                    "T",
                ]
    },
    {
        'filename': 'add_mle.java',
        'lang': 'Java',
                'expected': [
                    "!",
                    "!",
                    "!",
                ]
    },
    {
        'filename': 'add_wrong.java',
        'lang': 'Java',
                'expected': [
                    "W",
                    "C",
                    "W",
                ]
    },
    {
        'filename': 'add.java',
        'lang': 'Java',
                'expected': [
                    "C",
                    "C",
                    "C",
                ]
    },
    {
        'filename': 'add.py',
        'lang': 'Python',
                'expected': [
                    "C",
                    "C",
                    "C",
                ]
    },
    {
        'filename': 'add_wrong.py',
        'lang': 'Python',
                'expected': [
                    "C",
                    "W",
                    "W",
                ]
    }
]

test1 = [
    {
        'filename': 'david_prob3_plat.cpp',
        'lang': 'C++',
        'expected': [
            "C"
        ] * 22
    }
]


def main():
    print('Testing problem upload...')
    files = ['prob3_platinum_open22.zip', 'test_addition.zip']
    url = 'http://localhost:6969/problems/upload/testeventid/1'
    for file in files:
        print(f"Testing {file}...")
        r = send_problem(file, url)
        print(r)
        assert r.status_code == 200, "Status code is not 200"
        print(r.json())
        print("Test passed")
    print('All tests passed')
    print('-------------------------------')
    print('Testing grading system...')
    url = 'http://localhost:6969/grading/testeventid/0'
    for test in tests:
        print("Testing {}...".format(test['filename']))
        r = send_solution(test['filename'], test['lang'], url)
        print(r)
        assert r.status_code == 200, "Status code is not 200"
        print(r.json())
        for i, expected in enumerate(test['expected']):
            assert r.json()[
                i]['result'] == expected, f"Test {i} failed: expected {expected}, got {r.json()[i]['result']}"
    print('All tests passed')
    print('-------------------------------')
    print('Testing uploaded problem...')
    url = 'http://localhost:6969/grading/testeventid/1'
    for test in test1:
        print("Testing {}...".format(test['filename']))
        r = send_solution(test['filename'], test['lang'], url)
        print(r)
        assert r.status_code == 200, "Status code is not 200"
        print(r.json())
        for i, expected in enumerate(test['expected']):
            assert r.json()[
                i]['result'] == expected, f"Test {i} failed: expected {expected}, got {r.json()[i]['result']}"
        print('All tests passed')


if __name__ == '__main__':
    main()
