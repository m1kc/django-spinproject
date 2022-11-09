from ..generic.dicts_merging import merge_dicts
from ..project_manager.project_info import ProjectInfo
from ..generic.extended_jinja_environment import ExtendedEnvironment

import os
from abc import ABC, abstractmethod
from typing import Iterable, Sequence


class Module(ABC):
	name = ''
	help_text = ""
	contents = ()

	@classmethod
	@abstractmethod
	def last_version(cls) -> int: ...

	@classmethod
	@abstractmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None: ...

	@classmethod
	@abstractmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None: ...


class ExpectedContentMixin:
	contents = ()
	templates_label = 'templates'

	@classmethod
	def get_expected_content(cls, current_version: int) -> dict:
		content = cls.contents[current_version]

		if current_version == 0:
			return {key: (value, ) for key, value in content[cls.templates_label].items()}

		return merge_dicts(
			cls.contents[current_version - 1][cls.templates_label],
			content[cls.templates_label],
		)


class JinjaExpectedContentMixin:
	environments: Sequence[ExtendedEnvironment] = ()

	@classmethod
	def get_expected_content(cls, current_version: int, templates_as_strings: bool = False) -> dict:
		if current_version == 0:
			templates_dict = cls.environments[current_version].get_templates_dict(templates_as_strings)
			return {filename: (template, ) for filename, template in templates_dict.items()}

		return merge_dicts(
			cls.environments[current_version - 1].get_templates_dict(templates_as_strings),
			cls.environments[current_version].get_templates_dict(templates_as_strings),
		)


class CleaningDirMixin:
	"""
	Adds a method for cleaning the directory.

	If there are files in the directory that do not belong to the module, they will NOT be deleted.
	If there are NO files in the directory that do not belong to the module, then the entire directory will be deleted.
	"""
	files_dir: str

	@classmethod
	def clean_dir(cls, files_to_remove: Iterable[str], files_dir: str = '') -> None:
		files_path = os.path.join(os.getcwd(), cls.files_dir if not files_dir else files_dir)

		for filename in files_to_remove:
			file_path = os.path.join(files_path, filename)

			if os.path.exists(file_path):
				os.remove(file_path)

			elif os.path.islink(file_path):
				os.unlink(file_path)

		if not os.listdir(files_path):
			os.rmdir(files_path)
