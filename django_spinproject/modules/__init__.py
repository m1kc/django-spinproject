from .gitignore import GitignoreModule
from .srta import SRTAModule
from .pytest import PytestModule


MODULES = {
	'gitignore': GitignoreModule,
	'srta': SRTAModule,
	'pytest': PytestModule,
}
