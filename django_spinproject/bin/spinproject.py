#!/usr/bin/env python3

from ..project_manager.project_info_manager import ProjectInfoManager
from ..generic.exit import exit_with_output

import os
import sys
import subprocess


EXTENDED_ARGUMENTS = {
	'init': '--init',
	'enable': '--enable',
	'disable': '--disable',
	'upgrade': '--upgrade',
}
HELP_MESSAGE = f"""
Usage:
  startproject.py <path>

Advanced usage:
  startproject.py {EXTENDED_ARGUMENTS['init']}
	initialize project info file

  startproject.py {EXTENDED_ARGUMENTS['enable']} MODULE_NAME
	enable specified module

  startproject.py {EXTENDED_ARGUMENTS['disable']} MODULE_NAME
	disable specified module. after disable module files can be removed

  startproject.py {EXTENDED_ARGUMENTS['upgrade']} [MODULE_NAMES...]
	upgrade all or specified modules

Allowed modules:
  gitignore
	creates ".gitignore" file 

Settings directory will be called `main`. You can override this
by passing 2nd argument (deprecated)."""


def main():
	argv = sys.argv[1:]

	if argv == ['-h'] or argv == ['--help']:
		print(HELP_MESSAGE)
		return

	elif EXTENDED_ARGUMENTS['init'] in argv:
		if len(argv) != 1:
			exit_with_output(f"The {EXTENDED_ARGUMENTS['init']} option does not support arguments", 2)

		ProjectInfoManager.init()
		return

	elif EXTENDED_ARGUMENTS['enable'] in argv:
		if len(argv) != 2 or argv[0] != EXTENDED_ARGUMENTS['enable']:
			exit_with_output(f"Incorrect format of '{EXTENDED_ARGUMENTS['enable']} MODULE_NAME' option", 2)

		ProjectInfoManager.enable_module(argv[1])
		return

	elif EXTENDED_ARGUMENTS['disable'] in argv:
		if len(argv) != 2 or argv[0] != EXTENDED_ARGUMENTS['disable']:
			exit_with_output(f"Incorrect format of '{EXTENDED_ARGUMENTS['disable']} MODULE_NAME' option", 2)

		ProjectInfoManager.disable_module(argv[1])
		return

	elif EXTENDED_ARGUMENTS['upgrade'] in argv:
		if len(argv) > 1 and argv[0] != EXTENDED_ARGUMENTS['upgrade']:
			exit_with_output(f"Incorrect format of '{EXTENDED_ARGUMENTS['upgrade']} [MODULE_NAMES...]' option", 2)

		ProjectInfoManager.upgrade_modules(*argv[1:])
		return

	elif len(argv) not in (1, 2):
		# Some extended arguments can accept an unlimited arguments number but the basic algorithm only works with two
		exit_with_output(HELP_MESSAGE, 2)

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
