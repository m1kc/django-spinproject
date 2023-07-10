from ._base import BaseModule
from .dockerignore_data import _V1_ENV, _V2_ENV, _V3_ENV


class DockerignoreModule(BaseModule):
	name = 'dockerignore'
	help_text = "Creates .dockerignore file"
	environments = (_V1_ENV, _V2_ENV, _V3_ENV)
