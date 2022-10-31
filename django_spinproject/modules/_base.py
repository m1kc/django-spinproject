from abc import ABC, abstractmethod


class Module(ABC):
	@classmethod
	@abstractmethod
	def last_version(cls) -> int: ...

	@classmethod
	@abstractmethod
	def upgrade_step(cls, current_version: int) -> None: ...

	@classmethod
	@abstractmethod
	def cleanup(cls, current_version: int) -> None: ...
