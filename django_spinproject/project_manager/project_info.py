from ..generic.exit import exit_with_output
from ..generic.serializable_obj import SerializationTrait

import json
import os
from typing import Union, Optional


DEFAULT_MAIN = 'main'


class ProjectInfoError(Exception):
	"""
	Basic class of errors when working with project information.
	"""
	...


class ProjectConfig(SerializationTrait):
	"""
	Stores the part about the project config.
	"""
	def __init__(self, project_name: str, main: str = DEFAULT_MAIN, module: Optional[dict] = None):
		self.project_name = project_name
		self.main = main
		self.module = module if module is not None else {}

	@classmethod
	def is_compatible(cls, other: dict) -> bool:
		"""
		Checks by duck typing whether the dictionary matches the class object.
		"""
		class_object_attrs = ('project_name', 'main', 'module')
		return len(set(other.keys()) & set(class_object_attrs)) == len(class_object_attrs)

	def serialize(self) -> dict:
		serialized_obj = super(ProjectConfig, self).serialize()

		for module_name in serialized_obj['module']:
			module_config = serialized_obj['module'][module_name]

			if isinstance(module_config, SerializationTrait):
				serialized_obj['module'][module_name] = module_config.serialize()

		return serialized_obj


class ProjectInfo(SerializationTrait):
	"""
	Stores all information about the project.

	Allows to dump data to disk and load from it.
	"""
	FILENAME = 'spinproject.json'		# Changing the filename in production will lead to errors
	CONFIG_LABEL = 'config'

	def __init__(self, project_name: str, main: str = DEFAULT_MAIN):
		self.config = ProjectConfig(project_name, main)
		self.modules = []
		self.config_version = 1
		self.migration_state = {}

	@classmethod
	def load(cls) -> 'ProjectInfo':
		"""
		Loads project info data from disk.
		"""
		try:
			with open(cls.FILENAME, mode='r') as file:
				new_instance = cls('')
				new_instance_data = json.load(file, object_hook=cls.project_objects_hook)

				for key in new_instance.__dict__.keys():
					if key in new_instance_data:
						new_instance.__setattr__(key, new_instance_data[key])

				try:
					new_instance.self_check()

				except ProjectInfoError as e:
					exit_with_output(str(e), 1)

				return new_instance

		except FileNotFoundError:
			exit_with_output(f"Unable to read the project info file. File {cls.FILENAME} doesn't exists", 1)

	def save(self, overwrite: bool = True) -> None:
		"""
		Saves an instance of the class to a project info file.

		Args:
			overwrite:
				If True (by default) - The file will be overwritten.
				If False - Checks the existence of project file before writing. If there is a file, the program will
					fail with an error.
		"""
		if not overwrite and self.check_project_file_existence():
			exit_with_output(f"{self.FILENAME} file already exists", 1)

		try:
			with open(self.FILENAME, mode='w') as file:
				json.dump(self.serialize(), file, indent=2)

		except PermissionError:
			exit_with_output("Unable to save project info. Permission denied", 1)

	@classmethod
	def project_objects_hook(cls, jdict: dict) -> Union[dict, ProjectConfig]:
		if cls.CONFIG_LABEL in jdict:
			if ProjectConfig.is_compatible(jdict[cls.CONFIG_LABEL]):
				jdict[cls.CONFIG_LABEL] = ProjectConfig(**jdict[cls.CONFIG_LABEL])

		return jdict

	@classmethod
	def check_project_file_existence(cls):
		return cls.FILENAME in os.listdir()

	def self_check(self) -> None:
		if sorted(self.modules) != sorted(self.migration_state.keys()):
			raise ProjectInfoError("Modules are inconsistent with migrations")
