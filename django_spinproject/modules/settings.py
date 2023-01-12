from ._base import BaseModule
from .settings_data import _V1_ENV, _V2_ENV
from ..generic.directory_cleaning import clean_dir
from ..project_manager.project_info import ProjectInfo

import os


class SettingsModule(BaseModule):
	name = 'settings'
	help_text = """Improves settings.py file and creates .env.example file.
Creates backup of settings.py file. If the backup exists, module does not update it.
"""
	environments = (_V1_ENV, _V2_ENV)
	settings_filename = 'settings.py'
	settings_backup_postfix = '.orig'

	@classmethod
	def _before_upgrade(cls, current_version: int, project_info: ProjectInfo) -> None:
		full_files_dir = cls.get_full_files_dir(project_info)

		if current_version == 0:
			# creating backup of settings file
			settings_orig_path = os.path.join(full_files_dir, cls.settings_filename)
			settings_backup_path = settings_orig_path + cls.settings_backup_postfix

			if os.path.exists(settings_orig_path) and not os.path.exists(settings_backup_path):
				os.replace(settings_orig_path, settings_backup_path)

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs['name'] = project_info.config.main
		super()._upgrade_step(current_version, project_info, **render_kwargs)

	@classmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None:
		if current_version > 0:
			full_files_dir = cls.get_full_files_dir(project_info)
			clean_dir(
				cls.environments[current_version - 1].list_templates(),
				cls.get_full_files_dir(project_info),
				False,
			)

			# restoring settings backup
			settings_backup_path = os.path.join(full_files_dir, cls.settings_filename + cls.settings_backup_postfix)

			if os.path.exists(settings_backup_path):
				os.replace(settings_backup_path, settings_backup_path.rstrip(cls.settings_backup_postfix))

	@classmethod
	def get_full_files_dir(cls, project_info: ProjectInfo):
		return os.path.join(project_info.config.main, cls.files_dir)
