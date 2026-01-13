# Commands for testing

FOLDER=qqqq

projectenv: project
	cd ${FOLDER}
	uv add django django-environ whitenoise
	uv run python3

project: clean
	./django_spinproject/bin/spinproject.py ${FOLDER}

clean:
	rm -rf ./${FOLDER}
