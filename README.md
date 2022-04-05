# django-spinproject

Opinionated version of `django-admin startproject` with some popular third-party packages. Starter pack includes:

* `whitenoise` for painless work with static files;
* `settings.py` file with `django-environ` support so you can define your databases and stuff with environment variables and `.env` files;
    * Also, mostly pre-configured (but still optional) app and SQL logging;
    * Also, `django-postgres-readonly` (in case you have R/O databases);
    * But otherwise, it's still your standard `settings.py` you used to see in every other project.
* `script/bootstrap` and other [scripts to rule them all](https://github.blog/2015-06-30-scripts-to-rule-them-all/) so your fellow developers and maintainers don't ask you how to run this thing. Current versions of these scripts optimized for use with [poetry](https://python-poetry.org/), but you can easily adapt them for any Python package manager;
* A basic `Dockerfile` (and `make` targets for its common usage patterns);
* `make lint` command for linting with flake8.

## Requirements

* \*nix system;
* `django-admin` installed and available from `$PATH`.

Generated files will work fine in Django >= 2.0, not tested in earlier versions.

## How to use

1. Install the package: `pip install django-spinproject`
2. `django-spinproject <path>`

## Planned features

(for requests, create an issue or drop me a line at m1kc@yandex.ru)

* Some CLI flags to switch off the things you don't need.

## Changelog

### v1.3.0: Regular release

* `74d6ff5` Fix Docker build failing because of new Debian release. Closes #12.
* `ce0255f` Set `CI=true` when running `cibuild`. Closes #15.
* `3d54ece` Dockerfile: run `migrate` on boot
* `f9700fd` Allow script/setup to create .env file. Closes #13.
* `13230bb` Add ruby-foreman to Docker image
* `180a360` Remove gunicorn options from Dockerfile. Closes #16.
* `d2bf875` Warn about psycopg2 dependency. Closes #10.
* `0d05f5e` Ignore *~ files. Closes #11.
* `3933d52` Use script/setup in CI. Closes #17.

**Full Changelog**: https://github.com/m1kc/django-spinproject/compare/v1.2.1...v1.3.0

### Jun 21, 2021

* pytest support 'cause you don't want to waste time on setting that up (give it a try: `script/test`);
* Always call the settings directory `main` 'cause that's the only way to keep people sane when switching projects;
* Add GitLab CI config generator 'cause you don't want to write one yourself;
* flake8 isn't expected to be installed on your host system anymore.

### Apr 16, 2021

* `.gitignore` to keep your VCS clean;
* `.dockerignore` to keep your Docker images clean;
* `make clean` to get rid of `__pycache__` files when you need that;
* No need to install `django-postgres-readonly` anymore.

### Feb 5, 2021

* To avoid confusion, `python3` executable is now used instead of `python`.

### Feb 20, 2020

* Makefile now includes an additional target, `lint`, for linting your project with `flake8`. Give it a try: `$ make lint`.
* Dockerfile now works properly with most recent version of Poetry.
