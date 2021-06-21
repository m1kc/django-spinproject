# Commands for testing

FOLDER=qqqq

projectenv: project
	cd ${FOLDER}
	poetry add django django-environ whitenoise
	poetry shell

project: clean
	./django_spinproject/bin/spinproject.py ${FOLDER}

clean:
	rm -rf ./${FOLDER}
