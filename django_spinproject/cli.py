from .modules import MODULES
from .generic.package import Distribution

import argparse
import textwrap


DESCRIPTION = """Opinionated version of django-admin startproject
that intends to go further and do things that startproject can't do
but most people will do anyway.
"""
MODULES_HELP = '  ' + '\n  '.join(map(lambda x: x + '\n    ' + MODULES[x].help_text.replace('\n', '\n    '), MODULES))
EPILOG = f"""Allowed modules:
{MODULES_HELP}
"""


def create_argparser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		prog='django-spinproject',
		description=DESCRIPTION,
		epilog=textwrap.dedent(EPILOG),
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	parser.add_argument(
		'directory',
		type=str,
		nargs='?',
		help="project destination directory (deprecated).",
	)
	parser.add_argument(
		'--create',
		dest='project_creation_data',
		metavar='PATH',
		help=f"create project in specified path.",
		action='store',
		type=str,
		nargs=1,
	)
	parser.add_argument(
		'--init',
		dest='init_project_info',
		help="initialize project info file.",
		action='store_true',
	)
	parser.add_argument(
		'--enable',
		dest='modules_to_enable',
		metavar='MODULE_TO_ENABLE',
		help="enable specified module(s). use 'all' to enable all available modules.",
		action='store',
		nargs='+',
		type=str,
		choices=['all'] + list(MODULES.keys()),
	)
	parser.add_argument(
		'--disable',
		dest='module_to_disable',
		help="disable specified module. after disable module files can be removed.",
		action='store',
		nargs=1,
		type=str,
		choices=MODULES.keys(),
	)
	parser.add_argument(
		'--upgrade',
		dest='modules_to_upgrade',
		metavar='MODULE_TO_UPGRADE',
		help="upgrade all or specified modules. if modules are not specified, then all modules will be upgraded.",
		action='store',
		nargs='*',
		type=str,
		choices=MODULES.keys(),
	)
	parser.add_argument('--version', action='version', version=str(Distribution(parser.prog)))

	return parser
