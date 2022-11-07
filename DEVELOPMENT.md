# Developer notes

## Install git version

```sh
pip install --user --upgrade 'git+https://github.com/m1kc/django-spinproject.git@master'
# poetry add 'git+https://github.com/m1kc/django-spinproject.git@master'
```

## Publishing a release

1. Bump version in pyproject.toml. Create a commit with message `v1.x.x`;
2. Create a tag named `v1.x.x` (using gitg), `git push --tags`;
3. `poetry build`
4. `poetry publish`
5. Write release notes ("Auto-generate" for changelog link, `git log --oneline --graph` to generate commit list).
