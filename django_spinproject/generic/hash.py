from hashlib import sha1


HASH_BLOCK_SIZE = 65536


def get_file_hash(file) -> str:
	"""
	Returns file hash as string.

	Notes:
		Changing the hashing function in production will lead to failures.
	"""
	hash_function = sha1()
	buffer = file.read(HASH_BLOCK_SIZE)

	while len(buffer) > 0:
		hash_function.update(buffer)
		buffer = file.read(HASH_BLOCK_SIZE)

	return str(hash_function.hexdigest())


def get_text_hash(text: str, encoding: str = 'utf-8') -> str:
	"""
	Returns text hash as string.

	Args:
		text: Source text to get the hash.
		encoding: Source text encoding. utf-8 by default.

	Notes:
		Changing the hashing function in production will lead to failures.
	"""
	return str(sha1(text.encode(encoding)).hexdigest())
