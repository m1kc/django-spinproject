from .hash import get_file_hash, get_text_hash

from os.path import exists as file_exists
from typing import Sequence


def upgrade_file_content(name_of_file_to_upgrade: str, expected_content: Sequence[str], new_content: str):
	"""
	Upgrades specified file content.

	Content of file will be changed if file doesn't exist or file content equal to expected content.
	"""
	if file_exists(name_of_file_to_upgrade):
		file_hash = get_existed_file_hash(name_of_file_to_upgrade)
		expected_content_hashes = tuple(map(get_text_hash, expected_content))

		if file_hash not in expected_content_hashes:
			raise ValueError('The file already exists with a different content')

	write_file_content(name_of_file_to_upgrade, new_content)


def get_existed_file_hash(filename: str) -> str:
	with open(filename, mode='rb') as file:
		return get_file_hash(file)


def write_file_content(filename: str, content: str) -> None:
	with open(filename, mode='w') as file:
		file.write(content)
