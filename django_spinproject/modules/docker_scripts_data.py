_V1_CONTENT = {
	'templates': {
		'x-dockerbuild': """#!/bin/bash
set -e
set -x

docker build -t '{repository_domain}:{port}/{company_name}/{image_name}' .
""",
		'x-dockerpush': """#!/bin/bash
set -e
set -x

docker push '{repository_domain}:{port}/{company_name}/{image_name}'
""",
	}
}
