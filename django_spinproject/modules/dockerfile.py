from ._base import Module, ExpectedContentMixin
from .dockerfile_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo

from os import remove as remove_file
from os.path import exists as file_exists
from typing import Optional


class DockerfileModule(Module, ExpectedContentMixin):
	name = 'dockerfile'
	help_text = "Creates Dockerfile"
	filename = 'Dockerfile'
	file_dir = '.'
	contents = (_V1_CONTENT, )

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		name = project_info.config.main
		content = cls.contents[current_version]

		for filename in content[cls.templates_label]:
			content[cls.templates_label][filename] = content[cls.templates_label][filename].format(name=name)

		expected_content = cls.get_expected_content(current_version)

		for filename in expected_content:
			expected_content[filename] = tuple(i.format(name=name) for i in expected_content[filename])

		upgrade_files_content(cls.file_dir, expected_content, content[cls.templates_label])

	@classmethod
	def cleanup(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		if current_version > 0 and file_exists(cls.filename):
			remove_file(cls.filename)
