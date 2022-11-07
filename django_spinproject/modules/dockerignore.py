from ._base import Module, ExpectedContentMixin
from .dockerignore_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo

from os import remove as remove_file
from os.path import exists as file_exists
from typing import Optional


class DockerignoreModule(Module, ExpectedContentMixin):
	filename = '.dockerignore'
	file_dir = '.'
	contents = (_V1_CONTENT, )

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		upgrade_files_content(cls.file_dir, expected_content, content[cls.templates_label])

	@classmethod
	def cleanup(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		if current_version > 0 and file_exists(cls.filename):
			remove_file(cls.filename)
