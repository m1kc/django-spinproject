_CONTENT = {
	'Dockerfile': '''FROM alang/django:2.1-python3

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

ENV DJANGO_SETTINGS_MODULE {{ name }}.settings
ENV DJANGO_APP={{ name }}

ENV GUNICORN_CMD_ARGS ""
# If you prefer to set gunicorn options in Dockerfile, it's done like this:
#ENV GUNICORN_CMD_ARGS "-t 600 -w1"

ENV DJANGO_MANAGEMENT_ON_START "migrate; collectstatic --noinput"

COPY . /usr/django/app'''
}
