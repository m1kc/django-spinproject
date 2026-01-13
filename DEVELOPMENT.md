# Developer notes

## Install git version

```sh
pipx install git+https://github.com/m1kc/django-spinproject.git@rc --force
# pip install --user --upgrade 'git+https://github.com/m1kc/django-spinproject.git@master'
# uv add 'git+https://github.com/m1kc/django-spinproject.git@master'
```

## Publish a release

1. Bump version in pyproject.toml. Create a commit with message `v3.x.x`;
2. Create a tag named `v3.x.x` (using gitg), `git push --tags`;
3. `uv build`
4. `source ~/alpha/uv-publish-token.fish`
5. `uv publish dist/django_spinproject-3.0.0rc1*`
6. Write release notes ("Auto-generate" for changelog link, `git log --oneline --graph` to generate commit list).
