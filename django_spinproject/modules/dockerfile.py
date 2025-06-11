from ._base import BaseModule
from .dockerfile_data import _V1_ENV, _V2_ENV, _V3_ENV, _V4_ENV, _V5_ENV
from ..project.project_info import ProjectInfo


class DockerfileModule(BaseModule):
	name = 'dockerfile'
	help_text = "Creates Dockerfile"
	environments = (_V1_ENV, _V2_ENV, _V3_ENV, _V4_ENV, _V5_ENV)

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs['name'] = project_info.config.main
		render_kwargs['base_image'] = project_info.config.docker.base_image
		super()._upgrade_step(current_version, project_info, **render_kwargs)
