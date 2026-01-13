_CONTENT = {
	'Dockerfile': '''FROM {{ base_image }}

# --allow-releaseinfo-change for cases when stable becomes oldstable
RUN apt-get update --allow-releaseinfo-change \\
    && apt-get install -y --no-install-recommends \\
        postgresql-client \\
        mariadb-client \\
        nano \\
        ruby-foreman \\
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --python-preference only-system

ENV DJANGO_SETTINGS_MODULE={{ name }}.settings
ENV DJANGO_APP={{ name }}

#ENV GUNICORN_CMD_ARGS="-t 600 -w1"
ENV GUNICORN_CMD_ARGS=""

ENV PATH="/.venv/bin:$PATH"

WORKDIR "/usr/django/app"
CMD ["script/run", "--production"]

COPY . /usr/django/app'''
}
