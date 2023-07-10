from .hash import get_file_hash, get_text_hash

import os
from typing import Sequence, Dict, Iterable


def upgrade_files_content(files_dir: str, expected_content: Dict[str, Sequence[str]], new_content: Dict[str, str]):
	"""
	Upgrades content in specified files.

	Args:
		files_dir: Path to directory where the files should be upgraded.
		expected_content: Dictionary of expected content in existing files.
		new_content: Dictionary of new content in all files.

	Raises:
		ValueError: If at least one file is modified.

	Notes:
		If the file does not exist during the upgrade, it will be added with the new content.
	"""
	check_existed_files(files_dir, expected_content)

	if not os.path.exists(files_dir):
		os.mkdir(files_dir)

	for filename in new_content:
		if files_dir[-1:] == '.':
			files_dir = files_dir.rstrip('/.')

		print(f"Writing {os.path.join(files_dir, filename)}...")
		file_path = os.path.join(files_dir, filename)
		write_file_content(file_path, new_content[filename])


def check_existed_files(files_dir: str, expected_content: Dict[str, Sequence[str]]):
	if not os.path.exists(files_dir):
		return

	for filename in expected_content:
		file_path = os.path.join(files_dir, filename)

		check_file_content(file_path, expected_content[filename])


def check_file_content(file_path: str, expected_content: Iterable[str]) -> None:
	if os.path.exists(file_path):
		existed_file_hash = get_existed_file_hash(file_path)
		expected_file_hashes = tuple(map(get_text_hash, expected_content))

		if existed_file_hash not in expected_file_hashes:
			raise ValueError(f"The file already exists with a different content. File: {file_path}")


def get_existed_file_hash(file_path: str) -> str:
	with open(file_path, mode='rb') as file:
		return get_file_hash(file)


def write_file_content(file_path: str, content: str) -> None:
	with open(file_path, mode='w') as file:
		file.write(content)
