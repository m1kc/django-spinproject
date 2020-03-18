# django-spinproject

Opinionated version of `startproject` with some popular third-party packages. Starter pack includes:

* `whitenoise` for painless work with static files;
* `settings.py` file with `django-environ` support so you can define your databases and stuff with environment variables and `.env` files;
    * Also, mostly pre-configured (but still optional) app and SQL logging;
    * Also, `django-postgres-readonly` (in case you have R/O databases);
    * But otherwise, it's still your standard `settings.py` you used to see in every other project.
* `script/bootstrap` and other [scripts to rule them all](https://github.blog/2015-06-30-scripts-to-rule-them-all/) so your fellow developers and maintainers don't ask you how to run this thing. Current versions of these scripts optimized for use with [poetry](https://python-poetry.org/), but you can easily adapt them for any Python package manager;
* A basic `Dockerfile` (and a `Makefile` for its common usage patterns).

## Requirements

* \*nix system;
* `django-admin` installed and available from `$PATH`.

Generated files will work fine in Django >= 2.0, not tested in earlier versions.

## How to use

Clone the repo, then run:

```
python3 spinproject.py <project name> <path>
```

Also, you can use `enhance-*` scripts separately (with the same parameters) if you only need to add one specific thing to existing project.
