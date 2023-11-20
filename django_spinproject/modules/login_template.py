from ._base import BaseModule
from .login_template_data import _V1_ENV
from ..project.project_info import ProjectInfo
from ..generic.exit import exit_with_output
from ..constants import DJANGO_TEMPLATES_DIR, DJANGO_REGISTRATION_DIR

import os


class LoginTemplateModule(BaseModule):
	name = 'login-template'
	help_text = "Creates template of login page in specified app"
	environments = (_V1_ENV, )

	@classmethod
	def get_full_files_dir(cls, project_info: ProjectInfo):
		app_name = cls.input(f"Please, enter the app name: ")
		app_path = os.path.join(os.getcwd(), app_name)

		if os.path.exists(app_path) and os.path.isdir(app_path):
			app_templates_path = os.path.join(app_path, DJANGO_TEMPLATES_DIR)
			app_login_template_path = os.path.join(app_templates_path, DJANGO_REGISTRATION_DIR)

			if not os.path.exists(app_templates_path):
				os.mkdir(app_templates_path)

			return app_login_template_path

		error_message = f"The \"{app_name}\" application was not found in the project"
		exit_with_output(cls.format_message(error_message), 1)

	@classmethod
	def _after_upgrade(cls, current_version: int, project_info: ProjectInfo) -> None:
		if current_version == 0:
			cls.print(f"""The login page template has been created, but that's not all yet.
First of all, create a URL path for authorization.
Add something like this to {project_info.config.main}/urls.py:
\"\"\"
from django.urls import path, include

urlpatterns += [
	path('accounts/', include('django.contrib.auth.urls')),
]
\"\"\"

Make sure templates are enabled in {project_info.config.main}/settings.py:
\"\"\"
TEMPLATES = [
	{{
		...
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		...
\"\"\"

Add 'login_required' decorator to your view functions:
\"\"\"
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
	...
\"\"\"

Use URLs /accounts/login and /accounts/logout to log in and out.

Also, you probably want to set LOGIN_REDIRECT_URL = '/' in settings.py.
""")
