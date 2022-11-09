from ._base import BaseModule
from .pg_readonly_data import _V1_ENV
from ..project_manager.project_info import ProjectInfo

import os


class PGReadonlyModule(BaseModule):
	name = 'pg-readonly'
	help_text = "Creates DatabaseWrapper class for readonly connection to Postgres"
	environments = (_V1_ENV, )
	files_dir = 'pg_readonly'

	@classmethod
	def get_full_files_dir(cls, project_info: ProjectInfo):
		return os.path.join(project_info.config.main, cls.files_dir)
