#!/usr/bin/env python3

import os
import sys
import subprocess

def main():
	argv = sys.argv[1:]
	if (len(argv) not in [1,2]) or (argv == ['-h']) or (argv == ['--help']):
		print('Usage:')
		print('  startproject.py <path>')
		print('')
		print('Settings directory will be called `main`. You can override this')
		print('by passing 2nd argument (deprecated).')
		sys.exit(2)

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
