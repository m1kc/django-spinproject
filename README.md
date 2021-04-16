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
2. `django-spinproject <project name> <path>`

Also, take a look at `enhance-*` scripts (parameters are the same) if you only need to add one specific thing to existing project.

## Planned features

(for requests, create an issue or drop me a line at m1kc@yandex.ru)

* Always call the main module `main`
* Gitlab CI config
* pytest support

## Changelog

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
