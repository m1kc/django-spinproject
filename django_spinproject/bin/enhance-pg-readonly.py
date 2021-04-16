#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv

print('WARNING: pg-readonly is currently in beta stage.')

os.mkdir(os.path.join(path, name, 'pg_readonly'))

templates = {
	"base.py": '''from django.db.backends.postgresql import base
class DatabaseWrapper(base.DatabaseWrapper):
	def get_new_connection(self, conn_params):
		conn = super(DatabaseWrapper, self).get_new_connection(conn_params)
		conn.set_session(readonly=True)
		return conn''',
}

import shlex

for key in templates:
	print(f'Writing {name}/pg_readonly/{key}...')
	with open(os.path.join(path, name, 'pg_readonly', key), 'w') as f:
		f.write(templates[key])

