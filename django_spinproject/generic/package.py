from importlib.metadata import distribution, PackageNotFoundError


class Distribution:
	"""
	Contains package information with default values.

	Attributes:
		package_name: Name of package.
		version: Installed package version.
		author: Author of package.
		license: Software distribution license.

	Args:
		distribution_name: Name of installed package whose data should be received.
	"""
	__slots__ = 'package_name', 'version', 'author', 'license'

	DEFAULT_PACKAGE_NAME = "UNKNOWN"
	DEFAULT_VERSION = "UNKNOWN"
	DEFAULT_SUMMARY = ""
	DEFAULT_AUTHOR = "UNKNOWN"
	DEFAULT_LICENSE = "UNKNOWN"

	package_name: str
	version: str
	author: str
	license: str

	def __init__(self, distribution_name: str):
		self.package_name = self.DEFAULT_PACKAGE_NAME
		self.version = self.DEFAULT_VERSION
		self.author = self.DEFAULT_AUTHOR
		self.license = self.DEFAULT_LICENSE

		self._load_distribution(distribution_name)

	def _load_distribution(self, distribution_name: str) -> None:
		try:
			dist = distribution(distribution_name)
			self.package_name = dist.metadata.get('Name', self.DEFAULT_PACKAGE_NAME)
			self.version = dist.version
			self.author = dist.metadata.get('Author', self.DEFAULT_AUTHOR)
			self.license = dist.metadata.get('License', self.DEFAULT_LICENSE)

		except PackageNotFoundError:
			pass

	def __str__(self) -> str:
		return f"""{self.package_name} {self.version}
License: {self.license}
Author: {self.author}
"""
