---
name: castorini-release
description: Use when publishing nuggetizer, ragnarok, or umbrela to PyPI or TestPyPI — covers version bumping, build verification, twine checks, TestPyPI dry-run, and production PyPI publish. Use before or during a release cycle.
---

# Castorini Release

PyPI/TestPyPI publish workflow for nuggetizer, ragnarok, and umbrela.

## Supported Repos

| Repo | Package Name | Current Build |
|------|-------------|---------------|
| nuggetizer | `nuggetizer` | setuptools + pyproject.toml |
| ragnarok | `ragnarok` | setuptools + pyproject.toml |
| umbrela | `umbrela` | setuptools + pyproject.toml |

## Release Workflow

```
1. Bump version
2. Build package (uv build)
3. Check package (twine check)
4. Publish to TestPyPI (dry-run)
5. Test install from TestPyPI
6. Publish to PyPI (production)
7. Tag release
```

## Reference Files

- `references/pypi-checklist.md` — Step-by-step checklist with commands

## Preflight Script

Run the preflight checks before publishing:

```bash
bash skills/castorini-release/scripts/preflight.sh <repo-path>
```

This verifies:
- Package builds successfully
- twine check passes (metadata, description rendering)
- No uncommitted changes
- Version is bumped from the last release

## Gotchas

- All three repos use `bumpver` for version management. Check `pyproject.toml` for the `[tool.bumpver]` config.
- `uv build` produces both sdist and wheel in `dist/`.
- TestPyPI and PyPI are separate registries — a successful TestPyPI upload doesn't mean PyPI will accept it.
- TestPyPI install may fail if dependencies aren't on TestPyPI. Use `--extra-index-url https://pypi.org/simple/` as fallback.
- Release notes belong in `docs/release-notes/` (umbrela) or repo-specific locations.
- Tag format varies: check each repo's convention before tagging.
