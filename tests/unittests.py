import requests


def post(url, **kwargs):
    return requests.post(url, **kwargs)


def send_solution(filename, lang, url):
    with open(filename, 'r') as f:
        return post(url, data={'lang': lang}, files={'file': f})


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


def main():
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
        print("Test passed")


if __name__ == '__main__':
    main()
