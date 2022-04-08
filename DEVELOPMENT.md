# Developer notes

## Publishing a release

1. Bump version in pyproject.toml. Create a commit with message `v1.x.x`;
2. Create a tag named `v1.x.x`;
3. `poetry build`
4. `poetry publish`
