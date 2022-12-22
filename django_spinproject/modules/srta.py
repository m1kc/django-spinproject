from ._base import BaseModule
from ._mixins import ChmodMixin
from .srta_data import (
	_V1_ENV, _V1_SYMLINKS,
	_V2_ENV, _V2_SYMLINKS,
)
from ..generic.directory_cleaning import clean_dir
from ..project_manager.project_info import ProjectInfo

import os
import shlex
import subprocess
from typing import Optional


class SRTAModule(BaseModule, ChmodMixin):
	name = 'srta'
	help_text = "Creates srta scripts and additional symlinks"
	environments = (_V1_ENV, _V2_ENV)
	symlinks = (_V1_SYMLINKS, _V2_SYMLINKS)
	files_dir = 'script'

	@classmethod
	def _after_upgrade(cls, current_version: int, project_info: ProjectInfo) -> None:
		cls.change_files_mode(current_version)
		full_path_to_dir = os.path.join(os.getcwd(), cls.get_full_files_dir(project_info))

		for link_name, scripts_name in cls.symlinks[current_version].items():
			link_path = os.path.join(full_path_to_dir, link_name)

			if not os.path.exists(link_path):
				print(f"Symlink: {link_name} -> {scripts_name}")
				subprocess.run(f"cd {shlex.quote(full_path_to_dir)}; ln -s {scripts_name} {link_name}", shell=True)
			else:
				print(f"Symlink: {link_name} -> {scripts_name} already exists")

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs['name'] = project_info.config.main
		super()._upgrade_step(current_version, project_info, **render_kwargs)

	@classmethod
	def cleanup(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		if current_version > 0:
			files = cls.environments[current_version - 1].list_templates()
			symlinks = list(cls.symlinks[current_version - 1].keys())
			clean_dir(files + symlinks, cls.get_full_files_dir(project_info))
