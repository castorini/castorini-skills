---
name: install-all
description: Use when onboarding to nuggetizer, ragnarok, or umbrela and you need development environment setup for one repo or several repos at once, including clone-if-needed, uv or pip installation paths, shared virtualenv reuse, and smoke tests.
metadata:
  version: 0.1.0
  visibility: public
---

# Install All

Unified development environment setup for the Castorini Python repos, whether the user wants one repo or several.

## Supported Repos

| Repo | PyPI Name | CLI Binary | GitHub |
|------|-----------|------------|--------|
| nuggetizer | `nuggetizer` | `nuggetizer` | `castorini/nuggetizer` |
| ragnarok | `pyragnarok` | `ragnarok` | `castorini/ragnarok` |
| umbrela | `umbrela` | `umbrela` | `castorini/umbrela` |

## Context Detection

1. If cwd is inside one of the 3 repos (check for `pyproject.toml` with matching project name) → install that one.
2. If the user explicitly asks for one repo, install only that repo.
3. If cwd is the monorepo root or elsewhere and the request is ambiguous → ask which repo(s) to install, or install all if the user says so.

## Prerequisites

- Python 3.11+
- Git (SSH access to `github.com:castorini`)

## uv Detection

```bash
command -v uv
```

If present, use uv silently. If absent, ask the user once: install uv or proceed with pip.

## Virtual Environment Preference

- Prefer a shared `.venv-shared` in the current workspace root over repo-local `.venv` directories.
- Before creating any environment, check whether `.venv-shared` already exists in the current workspace root and reuse it if present.
- Only fall back to a repo-local environment if the shared environment is unavailable or the user explicitly asks for isolation.

## Install Flow

1. Resolve which repository or repositories are in scope.
2. Clone any missing repositories with SSH access to `castorini/<repo>`.
3. Reuse `.venv-shared` when it already exists in the workspace root.
4. Prefer `uv` for sync and dependency-group support.
5. Fall back to `pip` only when `uv` is unavailable or the user explicitly asks.
6. Run the repo CLI `doctor --output json` smoke test after install.
7. Run `pre-commit install` in each repository after a source install.

## Post-Install (all source installs)

```bash
pre-commit install
```

## Reference Files

- `references/extras.md` — Per-repo optional dependency stacks
- `references/install-recipes.md` — Per-repo clone, install, and smoke-test command sequences

## Gotchas

- `uv sync --group dev` understands dependency groups; `pip install -e .` does not. If you fall back to pip, install dev tools manually.
- `ragnarok` uses the package name `pyragnarok` on PyPI even though the repo and CLI command are `ragnarok`.
- `umbrela` only needs Java 21 for `pyserini` evaluation workflows, not for the default cloud-oriented development install.
- When reusing `.venv-shared`, make sure it was created with a Python version compatible with the target repo instead of blindly reusing an older interpreter.
- Run smoke tests from inside the target repository so editable installs and local entry points resolve correctly.
