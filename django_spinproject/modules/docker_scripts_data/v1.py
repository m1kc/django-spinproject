_CONTENT = {
	'x-dockerbuild': """#!/bin/sh

show_help() {
	echo "usage: $0 [-t tag | --tag=tag | -n name | --name=name]"
	echo "Options and arguments:"
	echo "-h, --help          Show this message and exit"
	echo "-t, --tag string    Set the custom image tag (default: project tag)"
	echo "-n, --name string   Set the default image name (default: project image name)"
}

while [ $# -gt 0 ]; do
	case $1 in
		-h|--help)
			show_help
			exit 0
		;;
		-t)
			TAG="$2"
			shift
			shift
		;;
		--tag=*)
			TAG="${1#*=}"
			shift
		;;
		-n)
			NAME="$2"
			shift
			shift
		;;
		--name=*)
			NAME="${1#*=}"
			shift
		;;
		-*|--*)
			echo "Unknown option: '$1'"
			exit 1
		;;
		*)
			echo "$0 does not support positional arguments"
			exit 1
		;;
	esac
done

set -e
set -x

TAG=${TAG:-'{{ tag }}'}
NAME=${NAME:-'{{ repository }}{% if repository %}/{% endif %}{{ image }}'}

docker build -t "$NAME:$TAG" .
""",
	'x-dockerpush': """#!/bin/sh

show_help() {
	echo "usage: $0 [-t tag | --tag=tag | -n name | --name=name]"
	echo "Options and arguments:"
	echo "-h, --help          Show this message and exit"
	echo "-t, --tag string    Set the custom image tag (default: project tag)"
	echo "-n, --name string   Set the default image name (default: project image name)"
}

while [ $# -gt 0 ]; do
	case $1 in
		-h|--help)
			show_help
			exit 0
		;;
		-t)
			TAG="$2"
			shift
			shift
		;;
		--tag=*)
			TAG="${1#*=}"
			shift
		;;
		-n)
			NAME="$2"
			shift
			shift
		;;
		--name=*)
			NAME="${1#*=}"
			shift
		;;
		-*|--*)
			echo "Unknown option: '$1'"
			exit 1
		;;
		*)
			echo "$0 does not support positional arguments"
			exit 1
		;;
	esac
done

set -e
set -x

TAG=${TAG:-'{{ tag }}'}
NAME=${NAME:-'{{ repository }}{% if repository %}/{% endif %}{{ image }}'}

docker push "$NAME:$TAG"
""",
}
