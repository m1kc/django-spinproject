from .gitignore import GitignoreModule
from .srta import SRTAModule
from .pytest import PytestModule
from .dockerfile import DockerfileModule
from .dockerignore import DockerignoreModule
from .docker_scripts import DockerScriptsModule
from .gitlab_ci import GitlabCIModule
from .pg_readonly import PGReadonlyModule
from .settings import SettingsModule
from .login_template import LoginTemplateModule


MOST_COMMON_MODULES = {
	GitignoreModule.name: GitignoreModule,
	SRTAModule.name: SRTAModule,
	PytestModule.name: PytestModule,
	DockerfileModule.name: DockerfileModule,
	DockerignoreModule.name: DockerignoreModule,
	DockerScriptsModule.name: DockerScriptsModule,
	GitlabCIModule.name: GitlabCIModule,
	PGReadonlyModule.name: PGReadonlyModule,
	SettingsModule.name: SettingsModule,
}

LEAST_COMMON_MODULES = {
	LoginTemplateModule.name: LoginTemplateModule,
}

MODULES = {
	**MOST_COMMON_MODULES,
	**LEAST_COMMON_MODULES,
}
