# PyPI Release Checklist

## Pre-Release

```bash
# 1. Ensure clean state
git status  # should be clean
git pull origin main

# 2. Bump version
bumpver update --patch   # or --minor / --major
# This updates pyproject.toml and creates a commit

# 3. Run preflight
bash /path/to/castorini-skills/skills/castorini-release/scripts/preflight.sh .
```

## Build and Verify

```bash
# 4. Build
uv build
# Creates dist/<package>-<version>.tar.gz and dist/<package>-<version>-py3-none-any.whl

# 5. Twine check
twine check dist/*
# Verifies metadata, long_description rendering, classifiers
```

## TestPyPI (Dry Run)

```bash
# 6. Upload to TestPyPI
twine upload --repository testpypi dist/*
# Requires: ~/.pypirc with [testpypi] section, or TWINE_USERNAME/TWINE_PASSWORD env vars

# 7. Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  <package-name>==<version>

# 8. Smoke test
<package-name> doctor
<package-name> --version
```

## Production PyPI

```bash
# 9. Upload to PyPI
twine upload dist/*
# Requires: PyPI API token or ~/.pypirc with [pypi] section

# 10. Verify install
pip install <package-name>==<version>
<package-name> --version
```

## Post-Release

```bash
# 11. Tag the release
git tag -a "v<version>" -m "Release v<version>"
git push origin "v<version>"

# 12. Update release notes
# umbrela: docs/release-notes/
# rank_llm: README release section and docs/release-notes/
# nuggetizer/ragnarok: README or CHANGELOG
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `TWINE_USERNAME` | PyPI username (use `__token__` for API tokens) |
| `TWINE_PASSWORD` | PyPI API token |
| `TWINE_REPOSITORY_URL` | Override repository URL |

## bumpver Configuration

All four repos use `bumpver` in `pyproject.toml`:

```toml
[tool.bumpver]
current_version = "0.0.6"
version_pattern = "MAJOR.MINOR.PATCH"

[tool.bumpver.file_patterns]
"pyproject.toml" = ['version = "{version}"']
```

Commands:
```bash
bumpver update --patch   # 0.0.6 → 0.0.7
bumpver update --minor   # 0.0.6 → 0.1.0
bumpver update --major   # 0.0.6 → 1.0.0
```
