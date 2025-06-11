# Developer notes

## Install git version

```sh
pipx install git+https://github.com/m1kc/django-spinproject.git@rc --force
# pip install --user --upgrade 'git+https://github.com/m1kc/django-spinproject.git@master'
# uv add 'git+https://github.com/m1kc/django-spinproject.git@master'
```

## Publish a release

1. Bump version in pyproject.toml. Create a commit with message `v1.x.x`;
2. Create a tag named `v1.x.x` (using gitg), `git push --tags`;
3. `uv build`
4. `uv publish --token <private-token> dist/<filenames>`
5. Write release notes ("Auto-generate" for changelog link, `git log --oneline --graph` to generate commit list).
