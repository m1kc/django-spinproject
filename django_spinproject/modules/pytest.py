from ._base import BaseModule
from .pytest_data import _V1_ENV
from ..project_manager.project_info import ProjectInfo

from typing import Optional


class PytestModule(BaseModule):
	name = 'pytest'
	help_text = "Creates pytest.ini and .coveragerc files"
	environments = (_V1_ENV, )

	@classmethod
	def _after_upgrade(cls, current_version: int, project_info: Optional[ProjectInfo] = None) -> None:
		if current_version == 0:
			print(
				"""---
Note: manual installation of additional third-party packages is required.
These commands should do the trick:

 poetry add --dev pytest pytest-django pytest-cov

If you don't use poetry, other package manager will do, too.
---"""
			)
