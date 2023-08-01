from .exceptions import ProjectInfoError
from .sections.config import ProjectConfig as IProjectConfig, ProjectConfigV1, ProjectConfigV2
from .sections.docker import DockerConfig as IDockerConfig, DockerConfigV1, DockerConfigV2
from ..generic.version_registry import VersionRegistry
from ..generic.serialization import SerializationTrait, DeserializingCapable
from ..constants import DEFAULT_MAIN


VERSION_REGISTRY = VersionRegistry()


class ProjectInfo(SerializationTrait, DeserializingCapable):
	"""
	Stores all project information.
	"""
	CONFIG_LABEL = 'config'
	DOCKER_LABEL = 'docker'
	VERSION = None
	ProjectConfig = IProjectConfig
	DockerConfig = IDockerConfig

	def __init__(self, project_name: str, main: str = DEFAULT_MAIN):
		self.config = self.ProjectConfig(project_name, main)
		self.modules = []
		self.config_version = self.VERSION
		self.migration_state = {}

	def self_check(self) -> None:
		"""
		Checks the internal state of the project information.

		Raises:
			ProjectInfoError: If enabled modules are not specified in the migration and vice versa.
		"""
		if sorted(self.modules) != sorted(self.migration_state.keys()):
			raise ProjectInfoError("Modules are inconsistent with migrations")

	@classmethod
	def deserialize(cls, raw_data: dict) -> 'ProjectInfo':
		"""
		Deserializes specified raw data and returns ProjectInfo instance.

		Args:
			raw_data: Dictionary of project information values.

		Returns:
			ProjectInfo instance with data from raw_data param.

		Raises:
			ValueError: When 'config' section is not specified.
			ValueError: When 'docker' section is not specified.
		"""
		config_section = raw_data.get(cls.CONFIG_LABEL)

		if not isinstance(config_section, dict):
			raise ValueError("Wrong config section")

		docker_section = config_section.get(cls.DOCKER_LABEL, {})

		if not isinstance(docker_section, dict):
			raise ValueError("Wrong docker section")

		config_section[cls.DOCKER_LABEL] = cls.DockerConfig(**docker_section)
		config = cls.ProjectConfig(**config_section)

		instance = cls(config.project_name, config.main)
		instance.modules = raw_data['modules']
		instance.migration_state = raw_data['migration_state']
		instance.config = config

		return instance


@VERSION_REGISTRY.register
class ProjectInfoV1(ProjectInfo):
	ProjectConfig = ProjectConfigV1
	DockerConfig = DockerConfigV1
	VERSION = 1


@VERSION_REGISTRY.register
class ProjectInfoV2(ProjectInfo):
	ProjectConfig = ProjectConfigV2
	DockerConfig = DockerConfigV2
	VERSION = 2
