from ._base import Module, ExpectedContentMixin, CleaningDirMixin
from .docker_scripts_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content
from ..generic.serializable_obj import SerializationTrait
from ..project_manager.project_info import ProjectInfo

import os
import shlex
import subprocess
from typing import Optional


class DockerScriptsConfig(SerializationTrait):
	def __init__(
		self,
		repository_domain: str = 'docker.mycompany.local',
		port: str = '5000',
		company_name: str = 'mycompany',
		image_name: str = 'myimage',
	):
		self.repository_domain = repository_domain
		self.port = port
		self.company_name = company_name
		self.image_name = image_name


class DockerScriptsModule(Module, ExpectedContentMixin, CleaningDirMixin):
	contents = (_V1_CONTENT,)
	files_dir = 'script'
	project_config_key = 'docker_scripts'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def get_or_create_scripts_config(cls, project_info: ProjectInfo) -> DockerScriptsConfig:
		if hasattr(project_info.config, cls.project_config_key):
			scripts_config = getattr(project_info.config, cls.project_config_key)

			if not isinstance(scripts_config, SerializationTrait):
				return DockerScriptsConfig(**scripts_config)

		return DockerScriptsConfig()

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		scripts_config = cls.get_or_create_scripts_config(project_info)
		setattr(project_info.config, cls.project_config_key, scripts_config)

		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		full_path_to_dir = os.path.join(os.getcwd(), cls.files_dir)

		for filename in content[cls.templates_label]:
			file_template = content[cls.templates_label][filename]
			content[cls.templates_label][filename] = file_template.format(**scripts_config.__dict__)

		for filename in expected_content:
			expected_content[filename] = tuple(i.format(**scripts_config.__dict__) for i in expected_content[filename])

		upgrade_files_content(cls.files_dir, expected_content, content[cls.templates_label])

		for key in content[cls.templates_label]:
			script_path = os.path.join(full_path_to_dir, key)
			subprocess.run(f"chmod +x {shlex.quote(script_path)}", shell=True)

	@classmethod
	def cleanup(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		if current_version > 0:
			cls.clean_dir(cls.contents[current_version - 1][cls.templates_label])

		if cls.project_config_key in vars(project_info.config):
			delattr(project_info.config, cls.project_config_key)
