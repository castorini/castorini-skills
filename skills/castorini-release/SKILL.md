---
name: castorini-release
description: Use when publishing nuggetizer, ragnarok, or umbrela to PyPI or TestPyPI and you need the release sequence for version bumps, build checks, twine validation, TestPyPI dry-runs, or final production publishing.
metadata:
  version: 0.1.0
  visibility: public
---

# Castorini Release

PyPI/TestPyPI publish workflow for nuggetizer, ragnarok, and umbrela.

Start with the reference checklist and use the bundled preflight script before uploading anything.

## Reference Files

- `references/pypi-checklist.md` — Step-by-step checklist with commands
- `references/release-sequence.md` — Supported repos and the high-level release sequence

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

- All three repos use `bumpver`; confirm the version change landed in the tracked files before you build.
- `uv build` should be run from the package root, not from the monorepo root or a skill directory.
- A TestPyPI upload only proves packaging and upload credentials; it does not guarantee PyPI will accept the same distribution later.
- TestPyPI installs often need `--extra-index-url https://pypi.org/simple/` because transitive dependencies may not exist on TestPyPI.
- Tagging rules and release-note locations are not fully standardized across the repos, so verify the target repo before creating the final tag.
