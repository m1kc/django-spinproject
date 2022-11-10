from ._base import BaseModule
from .pytest_data import _V1_ENV
from ..project_manager.project_info import ProjectInfo

from typing import Optional


class PytestModule(BaseModule):
	name = 'pytest'
	help_text = "Creates pytest.ini and .coveragerc files"
	environments = (_V1_ENV, )

	@classmethod
	def _upgrade_step(cls, current_version: int, project_info: ProjectInfo, **render_kwargs) -> None:
		render_kwargs['name'] = project_info.config.main
		super()._upgrade_step(current_version, project_info, **render_kwargs)
