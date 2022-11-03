from ..generic.dicts_merging import merge_dicts

from abc import ABC, abstractmethod


class Module(ABC):
	contents = ()

	@classmethod
	@abstractmethod
	def last_version(cls) -> int: ...

	@classmethod
	@abstractmethod
	def upgrade_step(cls, current_version: int) -> None: ...

	@classmethod
	@abstractmethod
	def cleanup(cls, current_version: int) -> None: ...


class ExpectedContentMixin:
	contents = ()
	templates_label = 'templates'

	@classmethod
	def get_expected_content(cls, current_version: int) -> dict:
		content = cls.contents[current_version]

		if current_version == 0:
			return {key: (value, ) for key, value in content[cls.templates_label].items()}

		return merge_dicts(
			cls.contents[current_version - 1][cls.templates_label],
			content[cls.templates_label],
		)
