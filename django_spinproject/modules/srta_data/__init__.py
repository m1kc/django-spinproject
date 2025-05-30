from .v1 import _CONTENT as _V1_CONTENT, _SYMLINKS as _V1_SYMLINKS
from .v2 import _CONTENT as _V2_CONTENT, _SYMLINKS as _V2_SYMLINKS
from .v3 import _CONTENT as _V3_CONTENT, _SYMLINKS as _V3_SYMLINKS
from .v4 import _CONTENT as _V4_CONTENT, _SYMLINKS as _V4_SYMLINKS
from .v5 import _CONTENT as _V5_CONTENT, _SYMLINKS as _V5_SYMLINKS
from .v6 import _CONTENT as _V6_CONTENT, _SYMLINKS as _V6_SYMLINKS
from ...generic.extended_jinja_environment import ExtendedEnvironment

from jinja2 import DictLoader


_V1_ENV = ExtendedEnvironment(loader=DictLoader(_V1_CONTENT))
_V2_ENV = ExtendedEnvironment(loader=DictLoader(_V2_CONTENT))
_V3_ENV = ExtendedEnvironment(loader=DictLoader(_V3_CONTENT))
_V4_ENV = ExtendedEnvironment(loader=DictLoader(_V4_CONTENT))
_V5_ENV = ExtendedEnvironment(loader=DictLoader(_V5_CONTENT))
_V6_ENV = ExtendedEnvironment(loader=DictLoader(_V6_CONTENT))
