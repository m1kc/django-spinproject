from ._base import BaseModule
from .gitlab_ci_data import _V1_ENV, _V2_ENV, _V3_ENV
from ..project_manager.project_info import ProjectInfo


class GitlabCIModule(BaseModule):
	name = 'gitlab-ci'
	help_text = "Creates .gitlab-ci.yml file"
	environments = (_V1_ENV, _V2_ENV, _V3_ENV)

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs.update(project_info.config.docker.__dict__.copy())
		super()._upgrade_step(current_version, project_info, **render_kwargs)
