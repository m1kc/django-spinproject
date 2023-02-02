from ._base import BaseModule
from .dockerfile_data import _V1_ENV, _V2_ENV
from ..project_manager.project_info import ProjectInfo


class DockerfileModule(BaseModule):
	name = 'dockerfile'
	help_text = "Creates Dockerfile"
	environments = (_V1_ENV, _V2_ENV,)

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs['name'] = project_info.config.main
		super()._upgrade_step(current_version, project_info, **render_kwargs)
