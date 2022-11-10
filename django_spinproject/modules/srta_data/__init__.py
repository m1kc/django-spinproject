from .v1 import _CONTENT as _V1_CONTENT, _SYMLINKS as _V1_SYMLINKS
from ...generic.extended_jinja_environment import ExtendedEnvironment

from jinja2 import DictLoader


_V1_ENV = ExtendedEnvironment(loader=DictLoader(_V1_CONTENT))
