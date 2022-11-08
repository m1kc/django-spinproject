from typing import Sequence


class CompatibilityTrait:
	class_obj_attrs: Sequence[str] = ()

	@classmethod
	def is_compatible(cls, other: dict) -> bool:
		"""
		Checks the compatibility of the dictionary to the class object
		"""
		return len(set(other.keys()) & set(cls.class_obj_attrs)) == len(cls.class_obj_attrs)
