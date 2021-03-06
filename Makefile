# Commands for testing

NAME=qqqq
FOLDER=qqqq

projectenv: project
	bash -c 'cd ${FOLDER} && virtualenv ./virtualenv && source virtualenv/bin/activate && pip install django django-environ whitenoise'

project: clean
	./spinproject.py ${NAME} ${FOLDER}

clean:
	rm -rf ./${FOLDER}
