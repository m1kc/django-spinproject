from ._base import Module, ExpectedContentMixin, CleaningDirMixin
from .docker_scripts_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..project_manager.project_info import ProjectInfo, DockerConfig

import os
import shlex
import subprocess


class DockerScriptsModule(Module, ExpectedContentMixin, CleaningDirMixin):
	name = 'docker-scripts'
	help_text = "Creates scripts for building and pushing docker image"
	contents = (_V1_CONTENT,)
	files_dir = 'script'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		docker_config = project_info.config.docker
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		full_path_to_dir = os.path.join(os.getcwd(), cls.files_dir)

		for filename in content[cls.templates_label]:
			template = content[cls.templates_label][filename]
			content[cls.templates_label][filename] = cls.format_template(template, docker_config)

		for filename in expected_content:
			expected_content[filename] = tuple(cls.format_template(i, docker_config) for i in expected_content[filename])

		upgrade_files_content(cls.files_dir, expected_content, content[cls.templates_label])

		for key in content[cls.templates_label]:
			script_path = os.path.join(full_path_to_dir, key)
			subprocess.run(f"chmod +x {shlex.quote(script_path)}", shell=True)

	@classmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None:
		if current_version > 0:
			cls.clean_dir(cls.contents[current_version - 1][cls.templates_label])

	@staticmethod
	def format_template(template: str, config: DockerConfig):
		"""
		Formats the template with using params from config.
		"""
		args_to_fill = config.__dict__.copy()
		repository = args_to_fill['repository']
		args_to_fill['repository'] = repository + '/' if repository else ''

		return template.format(**args_to_fill)
