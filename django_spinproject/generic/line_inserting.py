def insert_line(text: str, line: str, line_number: int) -> str:
	"""
	Inserts line to specified line number of text.
	"""
	lines = text.split('\n')

	if line_number > len(lines) - 1:
		raise ValueError('The line number is greater than the number of lines in the text')

	lines.insert(line_number, line)

	return '\n'.join(lines)
