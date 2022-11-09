from ._base import BaseModule
from .pytest_data import _V1_ENV
from ..project_manager.project_info import ProjectInfo

from typing import Optional


class PytestModule(BaseModule):
	name = 'pytest'
	help_text = "Creates pytest.ini and .coveragerc files"
	environments = (_V1_ENV, )
