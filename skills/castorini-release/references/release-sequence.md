# Supported Repos and Release Sequence

## Supported Repos

| Repo | Package Name | Current Build |
|------|-------------|---------------|
| nuggetizer | `nuggetizer` | setuptools + pyproject.toml |
| ragnarok | `ragnarok` | setuptools + pyproject.toml |
| umbrela | `umbrela` | setuptools + pyproject.toml |

## Release Sequence

```text
1. Bump version
2. Build package with uv
3. Run twine check
4. Upload to TestPyPI
5. Test install from TestPyPI
6. Upload to PyPI
7. Tag the release
```
