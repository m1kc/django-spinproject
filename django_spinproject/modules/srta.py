from ._base import Module, ExpectedContentMixin
from .srta_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content

import os
import shutil
import shlex
import subprocess


class SRTAModule(Module, ExpectedContentMixin):
	contents = (_V1_CONTENT, )
	files_dir = 'script'
	symlinks_label = 'symlinks'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int) -> None:
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		full_path_to_dir = os.path.join(os.getcwd(), cls.files_dir)

		upgrade_files_content(cls.files_dir, expected_content, content[cls.templates_label])

		for key in content[cls.templates_label]:
			script_path = os.path.join(full_path_to_dir, key)
			subprocess.run(f"chmod +x {shlex.quote(script_path)}", shell=True)

		for key in content[cls.symlinks_label]:
			link_path = os.path.join(full_path_to_dir, key)

			if not os.path.exists(link_path):
				print(f"Symlink: {key} -> {content[cls.symlinks_label][key]}")
				subprocess.run(f"cd {shlex.quote(full_path_to_dir)}; ln -s {content[cls.symlinks_label][key]} {key}", shell=True)
			else:
				print(f"Symlink: {key} -> {content[cls.symlinks_label][key]} already exists")

	@classmethod
	def cleanup(cls, current_version: int) -> None:
		if current_version > 0:
			scripts_path = os.path.join(os.getcwd(), cls.files_dir)

			if os.path.exists(scripts_path):
				shutil.rmtree(scripts_path, ignore_errors=False, onerror=None)
