from typing import Dict, Union

from jinja2 import Environment, Template


class ExtendedEnvironment(Environment):
	def get_templates_dict(self, templates_as_strings: bool = False) -> Dict[str, Union[str, Template]]:
		"""
		Returns dictionary where keys are template names and values are templates.

		Args:
			templates_as_strings: Template conversion control flag.
				If False - returns templates as Template class objects.
				If True - returns templates as strings.
		"""
		res = {}

		for template_name in self.list_templates():
			if templates_as_strings:
				res[template_name] = self.get_template(template_name).render()
			else:
				res[template_name] = self.get_template(template_name)

		return res
