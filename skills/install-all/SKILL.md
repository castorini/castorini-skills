---
name: install-all
description: Set up development environments for nuggetizer, ragnarok, and/or umbrela. Detects which repo you're in or asks. Handles Python 3.11+, uv/pip, clone-if-needed, and smoke tests. Use when onboarding to any Castorini Python repo or setting up multiple repos at once.
---

# Castorini Install

Unified development environment setup for the Castorini Python repos.

## Supported Repos

| Repo | PyPI Name | CLI Binary | GitHub |
|------|-----------|------------|--------|
| nuggetizer | `nuggetizer` | `nuggetizer` | `castorini/nuggetizer` |
| ragnarok | `pyragnarok` | `ragnarok` | `castorini/ragnarok` |
| umbrela | `umbrela` | `umbrela` | `castorini/umbrela` |

## Context Detection

1. If cwd is inside one of the 3 repos (check for `pyproject.toml` with matching project name) → install that one.
2. If cwd is the monorepo root or elsewhere → ask which repo(s) to install, or install all if the user says so.

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

## Per-Repo Install

### nuggetizer

```bash
# Clone if needed
git clone git@github.com:castorini/nuggetizer.git

# uv path
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd nuggetizer
uv sync --group dev

# pip path
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd nuggetizer
pip install -e .
pip install pre-commit pytest mypy ruff

# Smoke test
nuggetizer doctor --output json
```

### ragnarok

```bash
# Clone if needed
git clone git@github.com:castorini/ragnarok.git

# uv path
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd ragnarok
uv sync --group dev --extra cloud

# pip path
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd ragnarok
pip install -e ".[cloud]"
pip install pre-commit pytest

# Smoke test
ragnarok doctor --output json
```

### umbrela

```bash
# Clone if needed
git clone git@github.com:castorini/umbrela.git

# uv path
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd umbrela
uv sync --group dev --extra cloud

# pip path
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd umbrela
pip install -e ".[cloud]"
pip install pre-commit pytest mypy ruff

# Smoke test
umbrela doctor --output json
```

## Post-Install (all source installs)

```bash
pre-commit install
```

## Reference Files

- `references/extras.md` — Per-repo optional dependency stacks

## Gotchas

| Repo | Pitfall |
|------|---------|
| nuggetizer | MyPy strict (`disallow_untyped_defs`); `[dependency-groups]` not pip-installable directly |
| ragnarok | PyPI name is `pyragnarok` not `ragnarok`; async-first design |
| umbrela | Java 21 only needed for `--extra pyserini` eval workflows |
| All | Dev dependency-groups require uv; with pip, install dev deps manually |
