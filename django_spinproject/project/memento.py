from .project_info import ProjectInfo, VERSION_REGISTRY
from .exceptions import ProjectInfoError
from .updater import ProjectInfoUpdater as BaseUpdater
from ..generic.exit import exit_with_output

import json
from os import listdir
from typing import Optional


class ProjectInfoMemento:
	"""
	Project info memento.

	Saves and loads project info.

	Notes:
		* By default, updates the loaded project info to the latest version.
	"""
	DEFAULT_PROJECT_FILE = 'spinproject.json'
	Updater = BaseUpdater

	def __init__(self, filename: Optional[str] = None):
		self.filename = filename or self.DEFAULT_PROJECT_FILE
		self.updater = self.Updater()

	def does_project_file_exist(self) -> bool:
		"""
		Checks for the presence of the project file.

		Returns:
			True if project file exists otherwise False.
		"""
		return self.filename in listdir()

	def save(self, info: ProjectInfo, overwrite: bool = True) -> None:
		"""
		Saves project info to project file.

		Args:
			info: Project info which to be saved.
			overwrite: Flag for overwriting the project file.
		"""
		serialization_settings = {}

		if not overwrite:
			if self.does_project_file_exist():
				exit_with_output(f"{self.filename} file already exists", 1)

			# If the project file is not overwritten, then a new project may be created.
			serialization_settings['is_initial'] = True

		try:
			with open(self.filename, mode='w') as file:
				json.dump(info.serialize(**serialization_settings), file, indent=2)

		except PermissionError:
			exit_with_output("Unable to save project info. Permission denied", 1)

	def load(self, update: bool = True) -> ProjectInfo:
		"""
		Loads project info from file.

		Args:
			update: Auto update flag. If True - Project info will be updated to the latest version.
				If False - Project info will be loaded without updating to the latest version.

		Returns:
			ProjectInfo instance.
		"""
		try:
			with open(self.filename, mode='r') as file:
				new_instance_data = json.load(file)

		except FileNotFoundError:
			exit_with_output(f"File {self.filename} doesn't exists", 1)

		config_version = new_instance_data.get('config_version')

		if config_version is None:
			exit_with_output(f"Unexpected config version: {config_version}", 1)

		project_info_cls = VERSION_REGISTRY[config_version]
		new_instance = project_info_cls.deserialize(new_instance_data)

		try:
			new_instance.self_check()

		except ProjectInfoError as e:
			exit_with_output(str(e), 1)

		if self.updater.can_be_updated(new_instance) and update:
			print('An outdated project file was found. Automatic update attempt.')
			new_instance = self.updater.update(new_instance)
			self.save(new_instance)

		return new_instance
