from ...generic.serialization import SerializationTrait

from warnings import warn
from abc import ABC


class DockerConfig(ABC, SerializationTrait):
	"""
	Contains docker config info.
	"""
	repository: str
	image: str
	tag: str
	username: str

	def __init__(
		self,
		repository='',			# docker.mycompany.local:5000
		image='myimage',		# mycompany/myimage
		tag='latest',
		username='user',
	):
		self.repository = repository
		self.image = image
		self.tag = tag
		self.username = username

	@property
	def is_blank(self) -> bool:
		return self.repository == ''


class DockerConfigV1(DockerConfig):
	pass


class DockerConfigV2(DockerConfig):
	base_image: str

	def __init__(
		self,
		repository='',			# docker.mycompany.local:5000
		image='myimage',		# mycompany/myimage
		tag='latest',
		username='user',
		base_image='python:3.9.6-slim-bullseye',
	):
		super().__init__(repository, image, tag, username)
		self.base_image = base_image

	@property
	def is_blank(self) -> bool:
		return super().is_blank or self.base_image == ''

	def __getattribute__(self, __name):
		if __name == 'username':
			warn(
				"The attribute 'username' of DockerConfig is deprecated and will not be used in future",
				DeprecationWarning,
				stacklevel=2,
			)

		return super().__getattribute__(__name)
