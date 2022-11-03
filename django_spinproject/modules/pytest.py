from ._base import Module, ExpectedContentMixin
from .pytest_data import _V1_CONTENT
from ..generic.file_upgrade import upgrade_files_content

import os


class PytestModule(Module, ExpectedContentMixin):
	contents = (_V1_CONTENT, )
	files_dir = '.'

	@classmethod
	def last_version(cls) -> int:
		return len(cls.contents)

	@classmethod
	def upgrade_step(cls, current_version: int) -> None:
		content = cls.contents[current_version]
		expected_content = cls.get_expected_content(current_version)
		upgrade_files_content(cls.files_dir, expected_content, content[cls.templates_label])

		if current_version == 0:
			print(
				"""---
Note: manual installation of additional third-party packages is required.
These commands should do the trick:

 poetry add --dev pytest pytest-django pytest-cov

If you don't use poetry, other package manager will do, too.
---"""
			)

	@classmethod
	def cleanup(cls, current_version: int) -> None:
		if current_version > 0:
			for filename in cls.contents[current_version - 1][cls.templates_label]:
				if os.path.exists(filename):
					os.remove(filename)
