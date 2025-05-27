from .v1 import _CONTENT as _V1_CONTENT
from ...generic.extended_jinja_environment import ExtendedEnvironment

from jinja2 import DictLoader


_V1_ENV = ExtendedEnvironment(loader=DictLoader(_V1_CONTENT))
