"""
Contains mixins for BaseModule.
"""
from ..generic.extended_jinja_environment import ExtendedEnvironment

import os
import shlex
import subprocess
from typing import Sequence


class ChmodMixin:
	files_dir = '.'
	environments: Sequence[ExtendedEnvironment] = ()

	@classmethod
	def change_files_mode(cls, current_version: int):
		"""
		Changes the files mode to "executable".
		"""
		cwd = os.getcwd()

		for filename in cls.environments[current_version - 1].list_templates():
			full_file_path = os.path.join(cwd, cls.files_dir, filename)
			subprocess.run(f"chmod +x {shlex.quote(full_file_path)}", shell=True)
