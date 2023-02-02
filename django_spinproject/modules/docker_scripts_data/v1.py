_CONTENT = {
	'x-dockerbuild': """#!/bin/bash
set -e
set -x

docker build -t '{{ repository }}{% if repository %}/{% endif %}{{ image }}:{{ tag }}' .
""",
	'x-dockerpush': """#!/bin/bash
set -e
set -x

docker push '{{ repository }}{% if repository %}/{% endif %}{{ image }}:{{ tag }}'
""",
}
