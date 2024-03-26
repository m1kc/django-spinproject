# Developer notes

## Install git version

```sh
pipx install git+https://github.com/m1kc/django-spinproject.git@rc --force
# pip install --user --upgrade 'git+https://github.com/m1kc/django-spinproject.git@master'
# poetry add 'git+https://github.com/m1kc/django-spinproject.git@master'
```

## Publish a release

1. Bump version in pyproject.toml. Create a commit with message `v1.x.x`;
2. Create a tag named `v1.x.x` (using gitg), `git push --tags`;
3. `poetry build`
4. `poetry publish`
5. Write release notes ("Auto-generate" for changelog link, `git log --oneline --graph` to generate commit list).

## Authenticate with PyPI

```sh
poetry config pypi-token.pypi <private-token>
```
