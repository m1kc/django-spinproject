from ...generic.serialization import SerializationTrait
from ...constants import DEFAULT_MAIN
from .docker import DockerConfig as IDockerConfig, DockerConfigV1, DockerConfigV2

from typing import Optional, Any
from warnings import warn
from abc import ABC


class ProjectConfig(ABC, SerializationTrait):
	"""
	Stores project config.
	"""
	DockerConfig = IDockerConfig
	project_name: str
	main: str
	module: dict
	docker: DockerConfig

	def __init__(
		self,
		project_name: str,
		main: str = DEFAULT_MAIN,
		module: Optional[dict] = None,
		docker: Optional[DockerConfig] = None,
	):
		self.project_name = project_name
		self.main = main
		self.module = module if module is not None else {}
		self.docker = docker or self.DockerConfig()

	def serialize(self) -> dict:
		serialized_obj = super(ProjectConfig, self).serialize()

		for module_name in serialized_obj['module']:
			module_config = serialized_obj['module'][module_name]

			if isinstance(module_config, SerializationTrait):
				serialized_obj['module'][module_name] = module_config.serialize()

		return serialized_obj

	def __getattribute__(self, __name: str) -> Any:
		attr = super().__getattribute__(__name)

		if __name == 'docker' and attr.is_blank:
			warn(
				"You are using a module that affects an empty \"docker\" section in the project file.\n"
				"Please specify your Docker image configuration parameters in the `spinproject.json` file "
				"otherwise it can lead to errors and unpredictable behavior."
			)

		return attr


class ProjectConfigV1(ProjectConfig):
	DockerConfig = DockerConfigV1


class ProjectConfigV2(ProjectConfig):
	DockerConfig = DockerConfigV2
