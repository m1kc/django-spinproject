def merge_dicts(a: dict, b: dict) -> dict:
	"""
	Merges two dictionaries by their keys, while the values are entered in the tuple.

	Examples:
		>>> a = {1: 1, 2: 2, 3: 3}
		>>> b = {3: 3, 4: 4, 5: 5}
		>>> merge_dicts(a, b)
		{
			1: (1, ),
			2: (2, ),
			3: (3, 3),
			4: (4, ),
			5: (5, ),
		}

	Notes:
		Does not guarantee the order of keys.
	"""
	res = {}

	for key in set(a.keys()) | set(b.keys()):
		values = []

		if key in a:
			values.append(a[key])

		if key in b:
			values.append(b[key])

		res[key] = tuple(values)

	return res
