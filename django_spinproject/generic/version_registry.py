from typing import Type, Dict, Optional


class VersionRegistry:
	"""
	Stores different versions of object classes.

	Examples:
		>>> registry = VersionRegistry()
		>>>
		>>> class A:
		>>> 	pass
		>>>
		>>> @registry.register
		>>> class AV1:
		>>> 	VERSION = 1
		>>>
		>>> class AV2:
		>>> 	VERSION = 2
		>>>
		>>> registry.register(AV2, 2)
		>>> registry.get_latest_version() is AV2
		True
		>>> registry[1] is AV1
		True
	"""
	VERSION_ATTR = 'VERSION'

	_version_map: Dict[int, Type]

	def __init__(self):
		self._version_map = {}

	def __getitem__(self, item: int) -> Type:
		"""
		Returns class by version.

		Args:
			item: Version which you need.

		Returns:
			Class which registered under specified version.

		Raises:
			KeyError: When requesting an unregistered version.
		"""
		return self._version_map[item]

	def register(self, cls: Type, version: Optional[int] = None) -> Type:
		"""
		Registers class under special version.

		Args:
			cls: Class to register.
			version: Version under which you need to register class.

		Returns:
			Registered class.

		Notes:
			Can be used as a decorator without parameters.

		Raises:
			ValueError: When registering a registered version.
			ValueError: When registering without specifying the version.
			ValueError: When class already registered.
		"""
		if version is None:
			version = getattr(cls, self.VERSION_ATTR, None)

		if version is None:
			raise ValueError('Version is not specified')

		if version in self._version_map:
			raise ValueError(f'Version: {version} already registered')

		if cls in self._version_map.values():
			raise ValueError(f'Class: {cls} already registered')

		self._version_map[version] = cls
		return cls

	def unregister(self, version: int) -> None:
		"""
		Deletes the specified version from the registry.

		Args:
			version: The version to be deleted.

		Returns:
			ValueError: When unregistered an unregistered version.
		"""
		if version not in self._version_map:
			raise ValueError(f'Version: {version} is not registered')

		del self._version_map[version]

	def get_latest_version_num(self) -> Optional[int]:
		"""
		Returns latest available version number.

		Returns:
			Latest version number or None if register is empty.
		"""
		if self._version_map:
			return max(self._version_map.keys())

		return None

	def get_latest_version(self) -> Optional[Type]:
		"""
		Returns latest class by version number.

		Returns:
			Class which registered under latest version number or None if register is empty.
		"""
		latest_version_num = self.get_latest_version_num()

		if latest_version_num is not None:
			return self._version_map[latest_version_num]

		return None
