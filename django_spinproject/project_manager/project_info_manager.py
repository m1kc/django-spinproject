from .project_info import ProjectInfo
from ..modules import MODULES
from ..generic.exit import exit_with_output

import os


def _check_module_existence(module_name: str) -> None:
	if module_name not in MODULES:
		exit_with_output(f"Module {module_name} doesn't exists", 1)


def check_module_existence(method):
	"""
	Decorator for checking the existence of a module.
	"""
	def inner(cls, module_name: str, *args, **kwargs):
		_check_module_existence(module_name)
		return method(cls, module_name, *args, **kwargs)

	return inner


def check_project_info_file_existence(method):
	"""
	Decorator for checking the existence of a project information file.
	"""
	def inner(cls, *args, **kwargs):
		if not ProjectInfo.check_project_file_existence():
			exit_with_output("Project is not initialized", 1)

		return method(cls, *args, **kwargs)

	return inner


def check_django_project_existence(method):
	"""
	Decorator of checking the existence of the Django project.
	"""
	def inner(cls, *args, **kwargs):
		if 'manage.py' not in os.listdir():
			exit_with_output(
				"Project not found\nMake sure that the command is called at the root of the django project",
				1,
			)

		return method(cls, *args, **kwargs)

	return inner


def ask_project_name() -> str:
	"""
	Polls the user until he specifies the name of the project.
	"""
	project_name = ""

	while not project_name:
		project_name = input("Enter project name (not used yet): ")

		if not project_name:
			print("Project name can't be empty")

	return project_name


class ProjectInfoManager:
	@classmethod
	@check_django_project_existence
	def init(cls) -> None:
		"""
		Initializes the project file.
		"""
		project_info = ProjectInfo(project_name=ask_project_name())
		project_info.save(overwrite=False)
		print("""Note: third-party packages are required for some modules.
These commands should do the trick:

 poetry init
 # For Django itself
 poetry add django
 # For its PostgreSQL adapter
 poetry add psycopg2-binary
 # For settings module
 poetry add django-environ whitenoise
 # For linter script
 poetry add --dev flake8
 # For pytest
 poetry add --dev pytest pytest-django pytest-cov

If you don't use poetry, other package manager will do, too.
""")

	@classmethod
	@check_django_project_existence
	@check_project_info_file_existence
	def enable_modules(cls, *modules_to_enable) -> None:
		project_info = ProjectInfo.load()

		for module_name in modules_to_enable:
			_check_module_existence(module_name)

			if module_name not in project_info.modules:
				project_info.modules.append(module_name)
				project_info.migration_state[module_name] = 0

		project_info.save()

		print(
			ENABLE_MODULE_MESSAGE_TEMPLATE.format(
				modules_as_list=', '.join(modules_to_enable),
				modules_as_args=' '.join(modules_to_enable),
			),
		)

	@classmethod
	@check_django_project_existence
	@check_project_info_file_existence
	@check_module_existence
	def disable_module(cls, module_name: str) -> None:
		project_info = ProjectInfo.load()

		if module_name in project_info.modules:
			MODULES[module_name].cleanup(project_info.migration_state[module_name], project_info)
			project_info.modules.remove(module_name)
			del project_info.migration_state[module_name]
			project_info.save()
			print(f"Successfully disabled module: {module_name}")
		else:
			exit_with_output(f"Module {module_name} already disabled", 1)

	@classmethod
	@check_django_project_existence
	@check_project_info_file_existence
	def upgrade_modules(cls, *modules_to_upgrade) -> None:
		project_info = ProjectInfo.load()

		if not modules_to_upgrade:
			modules_to_upgrade = project_info.modules

		else:
			modules_to_upgrade = set(modules_to_upgrade)
			module_names_intersection = set(project_info.modules) & modules_to_upgrade
			not_enabled_modules = modules_to_upgrade - set(module_names_intersection)

			if not_enabled_modules:
				exit_with_output(
					"Some modules are not enabled or don't exist and therefore cannot be upgraded\n"
					f"Modules: {','.join(not_enabled_modules)}",
					1,
				)

			modules_to_upgrade = module_names_intersection

		for module_name in modules_to_upgrade:
			_module_version_before_upgrade = project_info.migration_state[module_name]
			current_module_version = _module_version_before_upgrade
			module = MODULES[module_name]
			module_last_version = module.last_version()

			while current_module_version < module_last_version:
				try:
					module.upgrade_step(current_module_version, project_info)
					current_module_version += 1
					project_info.migration_state[module_name] = current_module_version
					project_info.save()

				except ValueError as e:
					exit_with_output(f"Failed to upgrade the module {module_name}. {e}", 1)

			if _module_version_before_upgrade != module_last_version:
				print(f"Successfully upgraded {module_name}: {_module_version_before_upgrade} -> {module_last_version}")


ENABLE_MODULE_MESSAGE_TEMPLATE = """Successfully enabled modules: {modules_as_list}

The modules was added to config, but migrations
were not run. Run them with:
    django-spinproject --upgrade {modules_as_args}"""
