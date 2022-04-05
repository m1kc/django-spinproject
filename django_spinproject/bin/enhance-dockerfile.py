#!/usr/bin/env python3

import os
import sys
import subprocess

argv = sys.argv[1:]
assert len(argv) == 2, 'Must provide: name, path'
name, path = argv


template = f'''FROM alang/django:2.1-python3

# --allow-releaseinfo-change because buster is now oldstable
RUN apt-get update --allow-releaseinfo-change \\
    && apt-get install -y --no-install-recommends \\
        postgresql-client \\
        mariadb-client \\
        nano \\
        ruby-foreman \\
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

ENV DJANGO_SETTINGS_MODULE {name}.settings
ENV DJANGO_APP={name}

ENV GUNICORN_CMD_ARGS ""
# If you prefer to set gunicorn options in Dockerfile, it's done like this:
#ENV GUNICORN_CMD_ARGS "-t 600 -w1"

ENV DJANGO_MANAGEMENT_ON_START "migrate; collectstatic --noinput"

COPY . /usr/django/app'''

print('Writing Dockerfile...')
with open(os.path.join(path, 'Dockerfile'), 'w') as f:
	f.write(template)

