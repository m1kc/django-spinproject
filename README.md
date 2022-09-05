# django-spinproject

Opinionated version of `django-admin startproject` that intends to go further and do things that startproject can't do but most people will do anyway. Here's what you get:

* ⚛️ **Whitenoise**: usually you don't need that during local development but one day you're going to deploy your project and find out that it ignores the `static/` folder when running under gunicorn — which is sorta fine because big applications usually serve static files separately via nginx. Smaller apps with small number of assets, however, usually serve them within the same process, which is what whitenoise is for.
* 🔧 **settings.py**: it's slightly modified to also understand environment variables and `.env` files. This functionality requires the `django-environ` package. Also, app logger is mostly pre-configured for you.
* 🔒 **Support for marking PostgreSQL databases as read-only**.
* 🧰 `script/bootstrap` and other [scripts to rule them all](https://github.blog/2015-06-30-scripts-to-rule-them-all/) so your fellow developers and maintainers don't ask you how to run this thing. Current versions of these scripts optimized for use with [poetry](https://python-poetry.org/), but you can easily adapt them for any Python package manager.
* 🏗️ **Dockerfile and .dockerignore**: one day your app will go to production, and we've got you covered.
* 🏛️ **Gitlab CI config**: CI is a good thing.
* ⚕️ **Pre-configured linter** so you can find some common problems automagically.
* 🏃 **Pre-configured pytest** because you are going to need unit tests one day.
* 🗃️ **Auto-checks if you forgot to create migrations** whenever you run tests or CI.
* *️⃣ **.gitignore**: well, you know why.

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

See the [Releases](https://github.com/m1kc/django-spinproject/releases) page.
