from ._base import Module, ExpectedContentMixin, CleaningDirMixin
from .pg_readonly_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo

import os


class PGReadonlyModule(Module, ExpectedContentMixin, CleaningDirMixin):
	name = 'pg-readonly'
	help_text = "Creates DatabaseWrapper class for readonly connection to Postgres"
	contents = (_V1_CONTENT, )
	files_dir = 'pg_readonly'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		upgrade_files_content(cls.get_full_files_dir(project_info), expected_content, content[cls.templates_label])

	@classmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None:
		if current_version > 0:
			cls.clean_dir(cls.contents[current_version - 1][cls.templates_label], cls.get_full_files_dir(project_info))

	@classmethod
	def get_full_files_dir(cls, project_info: ProjectInfo):
		return os.path.join(project_info.config.main, cls.files_dir)
