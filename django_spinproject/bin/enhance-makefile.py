#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv


template = f'''lint:
	flake8 --select=C,F,E101,E112,E502,E72,E73,E74,E9,W291,W6 --exclude=.cache,migrations


docker:
	# TODO: update tag
	# docker build -t 'docker.mycompany.local:5000/mycompany/lm-dash-backend' .

dockerpush: docker
	# TODO: update tag
	# docker push 'docker.mycompany.local:5000/mycompany/lm-dash-backend'

deploy: dockerpush
'''

print('Writing Makefile...')
with open(os.path.join(path, 'Makefile'), 'w') as f:
	f.write(template)

