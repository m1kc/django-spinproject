from ._base import Module, ExpectedContentMixin
from .settings_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo

import os


class SettingsModule(Module, ExpectedContentMixin):
	name = 'settings'
	help_text = """Improves settings.py file and creates .env.example file
  Creates backup of settings.py file. If the backup exists, module does not update it.
"""
	files_dir = '.'
	contents = (_V1_CONTENT, )
	settings_filename = 'settings.py'
	settings_backup_postfix = '.orig'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		name = project_info.config.main
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		full_files_dir = cls.get_full_files_dir(project_info)

		for filename in content[cls.templates_label]:
			content[cls.templates_label][filename] = content[cls.templates_label][filename].format(name=name)

		for filename in expected_content:
			expected_content[filename] = tuple(i.format(name=name) for i in expected_content[filename])

		if current_version == 0:
			settings_orig_path = os.path.join(full_files_dir, cls.settings_filename)
			settings_backup_path = settings_orig_path + cls.settings_backup_postfix

			if os.path.exists(settings_orig_path) and not os.path.exists(settings_backup_path):
				os.replace(settings_orig_path, settings_backup_path)

		upgrade_files_content(full_files_dir, expected_content, content[cls.templates_label])

		if current_version == 0:
			print(f"""---
Note: manual installation of third-party packages is required.
These commands should do the trick:

 cd "{os.getcwd()}"
 poetry init
 poetry add django
 poetry add django-environ whitenoise
 poetry add --dev flake8
 # Also, if you intend to use PostgreSQL
 poetry add psycopg2-binary

If you don't use poetry, other package manager will do, too.
---""")

	@classmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None:
		if current_version > 0:
			full_files_dir = cls.get_full_files_dir(project_info)

			for filename in cls.contents[current_version - 1][cls.templates_label]:
				file_path = os.path.join(full_files_dir, filename)

				if os.path.exists(file_path):
					os.remove(file_path)

			settings_backup_path = os.path.join(full_files_dir, cls.settings_filename + cls.settings_backup_postfix)

			if os.path.exists(settings_backup_path):
				os.replace(settings_backup_path, settings_backup_path.rstrip(cls.settings_backup_postfix))

	@classmethod
	def get_full_files_dir(cls, project_info: ProjectInfo):
		return os.path.join(project_info.config.main, cls.files_dir)
