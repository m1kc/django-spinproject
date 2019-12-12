#!/usr/bin/env python

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv


template = f'''docker:
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

