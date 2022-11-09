from ._base import Module, JinjaExpectedContentMixin
from .dockerfile_data import _V1_ENV
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo

from os import remove as remove_file
from os.path import exists as file_exists
from typing import Optional


class DockerfileModule(Module, JinjaExpectedContentMixin):
	name = 'dockerfile'
	help_text = "Creates Dockerfile"
	filename = 'Dockerfile'
	file_dir = '.'
	environments = (_V1_ENV,)

	@classmethod
	def last_version(cls) -> int:
		return len(cls.environments)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		name = project_info.config.main
		content = {}

		for filename, template in cls.environments[current_version].get_templates_dict().items():
			content[filename] = template.render(name=name)

		expected_content = cls.get_expected_content(current_version)

		for filename, templates in expected_content.items():
			expected_content[filename] = tuple(i.render(name=name) for i in templates)

		upgrade_files_content(cls.file_dir, expected_content, content)

	@classmethod
	def cleanup(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		if current_version > 0 and file_exists(cls.filename):
			remove_file(cls.filename)
