from ._base import BaseModule
from ._mixins import ChmodMixin
from .docker_scripts_data import _V1_ENV
from ..project_manager.project_info import ProjectInfo


class DockerScriptsModule(BaseModule, ChmodMixin):
	name = 'docker-scripts'
	help_text = "Creates scripts for building and pushing docker image"
	environments = (_V1_ENV, )
	files_dir = 'script'

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs.update(project_info.config.docker.__dict__.copy())
		super()._upgrade_step(current_version, project_info, **render_kwargs)

	@classmethod
	def _after_upgrade(cls, current_version: int, project_info: ProjectInfo) -> None:
		cls.change_files_mode(current_version)
