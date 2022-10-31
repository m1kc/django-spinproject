from abc import ABC, abstractmethod


class Module(ABC):
	def last_version(self) -> int:
		return 0

	@abstractmethod
	def upgrade_step(self, current_version: int) -> None: ...

	@abstractmethod
	def cleanup(self, current_version: int) -> None: ...
