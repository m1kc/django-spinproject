from ..generic.serializable_obj import SerializationTrait
from ..project_manager.project_info import ProjectInfo


DOCKER_CONFIG_KEY = 'docker'		# Key of config in project_info.config.module
SUBSCRIBED_MODULES = []		# Contains module names who are subscribed to this config


class DockerConfig(SerializationTrait):
	def __init__(
		self,
		repository: str = '',		# docker.mycompany.local:5000
		image: str = 'myimage',		# mycompany/myimage
		tag: str = 'latest',
	):
		self.repository = repository
		self.image = image
		self.tag = tag


class DockerConfigMixin:
	"""
	Contains class methods for work with DockerConfig inside module
	"""
	name: str		# module name

	@classmethod
	def create_docker_config(cls, project_info: ProjectInfo) -> DockerConfig:
		"""
		Creates docker config object from existed or default data.

		Writes created object to project_info.config.module section.
		"""
		config = DockerConfig(**project_info.config.module.get(DOCKER_CONFIG_KEY, {}))
		project_info.config.module[DOCKER_CONFIG_KEY] = config
		return config

	@classmethod
	def remove_docker_config(cls, project_info: ProjectInfo) -> None:
		"""
		Removes docker config section from project info.
		"""
		subscribed_modules = set(SUBSCRIBED_MODULES)
		subscribed_modules.remove(cls.name)

		if not (set(project_info.modules) & set(subscribed_modules)):
			if DOCKER_CONFIG_KEY in project_info.config.module:
				del project_info.config.module[DOCKER_CONFIG_KEY]
