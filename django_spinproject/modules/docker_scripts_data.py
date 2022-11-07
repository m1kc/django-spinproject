_V1_CONTENT = {
	'templates': {
		'x-dockerbuild': """#!/bin/bash
set -e
set -x

docker build -t '{repository}{image}:{tag}' .
""",
		'x-dockerpush': """#!/bin/bash
set -e
set -x

docker push '{repository}{image}:{tag}'
""",
	}
}
