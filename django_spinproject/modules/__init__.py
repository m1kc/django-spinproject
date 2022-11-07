from .gitignore import GitignoreModule
from .srta import SRTAModule
from .pytest import PytestModule
from .dockerfile import DockerfileModule
from .dockerignore import DockerignoreModule
from .docker_scripts import DockerScriptsModule


MODULES = {
	'gitignore': GitignoreModule,
	'srta': SRTAModule,
	'pytest': PytestModule,
	'dockerfile': DockerfileModule,
	'dockerignore': DockerignoreModule,
	'docker_scripts': DockerScriptsModule,
}
