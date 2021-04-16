#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv

templates = {
	".dockerignore": '''**/__pycache__
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/azds.yaml
**/charts
**/docker-compose*
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml''',
}

import shlex

for key in templates:
	print(f'Writing {key}...')
	with open(os.path.join(path, key), 'w') as f:
		f.write(templates[key])

