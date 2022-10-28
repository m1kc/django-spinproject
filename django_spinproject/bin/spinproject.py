#!/usr/bin/env python3

import os
import sys
import subprocess
import json
from copy import deepcopy


PROJECT_INFO_FILENAME = 'spinproject.json'
PROJECT_INFO_TEMPLATE = {
	'config': {
		'project_name': '',
		'main': 'main',
	},
	'modules': [],
	'config_version': 1,
}


def init_project_info() -> None:
	"""
	Initializes the project file.
	"""
	cur_dir_files = os.listdir()
	project_check_file = 'manage.py'

	if project_check_file not in cur_dir_files:
		print('Project not found')
		print('Make sure that the command is called at the root of the django project')
		sys.exit(1)

	if PROJECT_INFO_FILENAME in cur_dir_files:
		print(f'{PROJECT_INFO_FILENAME} file already exists')
		sys.exit(1)

	project_info = deepcopy(PROJECT_INFO_TEMPLATE)
	project_info['config']['project_name'] = input('Enter project name: ')

	with open(PROJECT_INFO_FILENAME, mode='w') as file:
		json.dump(project_info, file, indent=2)


def main():
	argv = sys.argv[1:]
	if (len(argv) not in [1,2]) or (argv == ['-h']) or (argv == ['--help']):
		print('Usage:')
		print('  startproject.py <path>')
		print('')
		print('Advanced usage:')
		print('  startproject.py --init')
		print('    initialize project info file')
		print('')
		print('Settings directory will be called `main`. You can override this')
		print('by passing 2nd argument (deprecated).')
		sys.exit(2)

	elif '--init' in argv:
		if len(argv) != 1:
			print('The --init option does not support arguments')
			sys.exit(2)

		init_project_info()
		return

	name = 'main'
	path = argv[0]
	if len(argv) == 2:
		name = argv[1]

	print(f"Creating project at `{path}`")

	subprocess.run(['mkdir', '-p', path], check=True)
	subprocess.run(['django-admin', 'startproject', name, path], check=True)

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))


	active_modules = [
		'srta',
		'dockerfile',
		'makefile',
		'settings',
		# 'pytest',
		'gitignore',
		'dockerignore',
		'pg-readonly',
		'gitlab-ci',
		'pytest',
	]

	for m in active_modules:
		subprocess.run([os.path.join(BASE_DIR, f'enhance-{m}.py'), name, path], check=True)


if __name__ == '__main__':
	main()
