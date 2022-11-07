from ._base import Module, ExpectedContentMixin, CleaningDirMixin
from ._docker import DockerConfig, DockerConfigMixin, SUBSCRIBED_MODULES
from .gitlab_ci_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo

import os


class GitlabCIModule(Module, ExpectedContentMixin, CleaningDirMixin, DockerConfigMixin):
	name = 'gitlab-ci'
	help_text = "Creates .gitlab-ci.yml file"
	contents = (_V1_CONTENT, )
	filename = '.gitlab-ci.yml'
	file_dir = '.'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		docker_config = cls.create_docker_config(project_info)
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)

		for filename in content[cls.templates_label]:
			template = content[cls.templates_label][filename]
			content[cls.templates_label][filename] = cls.format_template(template, docker_config)

		for filename in expected_content:
			expected_content[filename] = tuple(cls.format_template(i, docker_config) for i in expected_content[filename])

		upgrade_files_content(cls.file_dir, expected_content, content[cls.templates_label])

	@classmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None:
		if current_version > 0 and os.path.exists(cls.filename):
			os.remove(cls.filename)

		cls.remove_docker_config(project_info)

	@staticmethod
	def format_template(template: str, config: DockerConfig) -> str:
		args_to_fill = config.__dict__.copy()
		repository = args_to_fill['repository']
		del args_to_fill['repository']
		args_to_fill['login_repository'] = repository
		args_to_fill['image_repository'] = repository + '/' if repository else ''

		return template.format(**args_to_fill)


SUBSCRIBED_MODULES.append(GitlabCIModule.name)
