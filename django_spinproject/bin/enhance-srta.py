#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv

os.mkdir(os.path.join(path, 'script'))

templates = {
	"bootstrap": '''#!/bin/bash
set -e
set -x

which python3 || which python
#which virtualenv
which poetry

poetry install''',
	
	"console": '''#!/bin/bash
set -e
set -x

poetry run python manage.py shell''',

	"server": '''#!/bin/bash
set -e
set -x

poetry run python manage.py runserver 0.0.0.0:8000''',

	"setup": '''#!/bin/bash
set -e
set -x

script/bootstrap

if [ -e db.sqlite3 ]; then
        mv db.sqlite3 db.sqlite3~
fi
poetry run python manage.py migrate''',

	"test": '''#!/bin/bash
set -e
set -x

echo "This project has no test suite."
#poetry run pytest''',

	"update": '''#!/bin/bash
set -e
set -x

script/bootstrap
poetry run python manage.py migrate''',
}

import shlex

for key in templates:
	print(f'Writing script/{key}...')
	with open(os.path.join(path, 'script', key), 'w') as f:
		f.write(templates[key])
	subprocess.run(f"chmod +x {shlex.quote(os.path.join(path, 'script', key))}", shell=True)

print('WARNING: skipped creating `cibuild` (not implemented)')
		       
symlinks = {
	'shell': 'console',
	'run': 'server',
}

for key in symlinks:
	fp = os.path.join(path, 'script')
	print(f'Symlink: {key} -> {symlinks[key]}')
	subprocess.run(f'cd {shlex.quote(fp)}; ln -s {symlinks[key]} {key}', shell=True)
