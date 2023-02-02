from ..generic.dicts_merging import merge_dicts
from ..project_manager.project_info import ProjectInfo
from ..generic.extended_jinja_environment import ExtendedEnvironment
from ..generic.file_upgrade import upgrade_files_content
from ..generic.directory_cleaning import clean_dir

from typing import Sequence, Dict, Tuple

from jinja2 import Template


class BaseModule:
	name = ''
	help_text = ""
	environments: Sequence[ExtendedEnvironment] = ()
	files_dir = '.'

	@classmethod
	def last_version(cls) -> int:
		"""
		Returns module last version number.
		"""
		return len(cls.environments)

	@classmethod
	def upgrade_step(cls, current_version: int, project_info: ProjectInfo) -> None:
		"""
		Upgrades module in project.
		"""
		cls._before_upgrade(current_version, project_info)
		cls._upgrade_step(current_version, project_info)
		cls._after_upgrade(current_version, project_info)

	@classmethod
	def _before_upgrade(cls, current_version: int, project_info: ProjectInfo) -> None:
		"""
		Contains the logic executed before upgrading the module.
		"""
		pass

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		"""
		Contains the module upgrade logic.
		"""
		content, expected_content = {}, {}

		for filename, template in cls.environments[current_version].get_templates_dict().items():
			content[filename] = template.render(render_kwargs)

		for filename, templates in cls.get_expected_templates(current_version).items():
			expected_content[filename] = tuple(i.render(render_kwargs) for i in templates)

		upgrade_files_content(cls.get_full_files_dir(project_info), expected_content, content)

	@classmethod
	def _after_upgrade(cls, current_version: int, project_info: ProjectInfo) -> None:
		"""
		Contains the logic executed after upgrading the module.
		"""
		pass

	@classmethod
	def cleanup(cls, current_version: int, project_info: ProjectInfo) -> None:
		"""
		Deletes module files.
		"""
		if current_version > 0:
			clean_dir(cls.environments[current_version - 1].list_templates(), cls.get_full_files_dir(project_info))

	@classmethod
	def get_expected_templates(cls, current_version: int) -> Dict[str, Tuple[Template]]:
		"""
		Returns templates of expected files on the current version of the module.
		"""
		if current_version == 0:
			templates_dict = cls.environments[current_version].get_templates_dict()
			return {filename: (template,) for filename, template in templates_dict.items()}

		return merge_dicts(
			cls.environments[current_version - 1].get_templates_dict(),
			cls.environments[current_version].get_templates_dict(),
		)

	@classmethod
	def get_full_files_dir(cls, project_info: ProjectInfo) -> str:
		"""
		Returns the full, but not absolute, path to the module files. The root is the project dir.
		"""
		return cls.files_dir
