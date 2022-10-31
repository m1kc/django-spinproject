import sys


def exit_with_output(message: str, exit_code: int = 0):
	print(message)
	sys.exit(exit_code)
