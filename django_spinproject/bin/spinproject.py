#!/usr/bin/env python3

from ..project_manager.project_info_manager import ProjectInfoManager
from ..generic.exit import exit_with_output
from ..cli import create_argparser
from ..modules import MODULES
from ..constants import DEFAULT_MAIN

import os
import subprocess


def main():
	argparser = create_argparser()
	args = argparser.parse_args()

	if args.directory is not None:
		exit_with_output("""Please use the new syntax:
  django-spinproject --create <path_to_project>

Old-style syntax is only available in versions < 2.""")

	elif args.project_creation_data is not None:
		path = args.project_creation_data[0]
		name = DEFAULT_MAIN

		subprocess.run(['mkdir', '-p', path], check=True)
		subprocess.run(['django-admin', 'startproject', name, path], check=True)
		os.chdir(path)
		ProjectInfoManager.init()
		print(f'''Created new project at path: {path}

Use django-spinproject --help to see which modules are available,
turn them on with --enable.

Edit spinproject.json to configure project settings.

Happy hacking!''')

	elif args.init_project_info:
		ProjectInfoManager.init()
		print(f'''Use django-spinproject --help to see which modules are available,
turn them on with --enable.

Edit spinproject.json to configure project settings.

Happy hacking!''')

	elif args.modules_to_enable is not None:
		if args.modules_to_enable[0] == 'all':
			modules_to_enable = list(MODULES.keys())
		else:
			modules_to_enable = args.modules_to_enable

		ProjectInfoManager.enable_modules(*modules_to_enable)

	elif args.module_to_disable is not None:
		ProjectInfoManager.disable_module(args.module_to_disable[0])

	elif args.modules_to_upgrade is not None:
		ProjectInfoManager.upgrade_modules(*args.modules_to_upgrade)

	else:
		argparser.print_help()
		argparser.exit(1)


if __name__ == '__main__':
	main()
