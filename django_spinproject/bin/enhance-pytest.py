#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv

templates = {
	"pytest.ini": '''[pytest]
DJANGO_SETTINGS_MODULE = main.settings
python_files = tests.py test_*.py *_tests.py *_test.py
# feel free to replace `term` with `term:skip-covered`
addopts = --cov=. --cov-config=.coveragerc --cov-report term --cov-report html --cov-report xml
''',
	".coveragerc": '''[run]
omit = */migrations/*, main/*, manage.py
''',
}

import shlex

for key in templates:
	print(f'Writing {key}...')
	with open(os.path.join(path, key), 'w') as f:
		f.write(templates[key])


print(f"""---
Note: manual installation of additional third-party packages is required.
This commands should do the trick:

 poetry add --dev pytest pytest-django pytest-cov

If you don't use poetry, other package manager will do, too.
---""")
