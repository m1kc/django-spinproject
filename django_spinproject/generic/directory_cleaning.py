import os
from typing import Iterable


def clean_dir(files_to_remove: Iterable[str], files_dir: str = '.', delete_empty_dir: bool = True) -> None:
	"""
	Deletes specified files in specified dir. If dir is empty after cleaning it will be deleted.

	Args:
		files_to_remove: Files to deleting.
		files_dir: Dir name where files are stored.
			Do not use the full path because it is set by default.
		delete_empty_dir: Flag for deleting an empty directory after cleaning.
	"""
	files_path = os.path.join(os.getcwd(), files_dir)

	for filename in files_to_remove:
		file_path = os.path.join(files_path, filename)

		if os.path.exists(file_path):
			os.remove(file_path)

		elif os.path.islink(file_path):
			os.unlink(file_path)

	if not os.listdir(files_path) and delete_empty_dir:
		os.rmdir(files_path)
