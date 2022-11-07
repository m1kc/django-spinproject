class SerializationTrait:
	"""
	Allows to serialize objects, including nested data structures if they are inherited from this class.
	"""
	def serialize(self) -> dict:
		serialized_obj = {}

		for key, value in self.__dict__.items():
			if isinstance(value, SerializationTrait):
				serialized_obj[key] = value.serialize()
			else:
				serialized_obj[key] = value

		return serialized_obj
