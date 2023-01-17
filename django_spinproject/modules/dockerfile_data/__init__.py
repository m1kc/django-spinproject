from .v1 import _CONTENT as _V1_CONTENT
from .v2 import _CONTENT as _V2_CONTENT
from ...generic.extended_jinja_environment import ExtendedEnvironment

from jinja2 import DictLoader


_V1_ENV = ExtendedEnvironment(loader=DictLoader(_V1_CONTENT))
_V2_ENV = ExtendedEnvironment(loader=DictLoader(_V2_CONTENT))
