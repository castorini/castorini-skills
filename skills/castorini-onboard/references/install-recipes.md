# Per-Repo Install Recipes

Use these only after the `castorini-onboard` skill has already triggered and the target repo set is known.

## Shared Source Install Pattern

With `uv`:

```bash
git clone git@github.com:castorini/<repo>.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd <repo>
uv sync --group dev <default-extras>
<cli> doctor --output json
pre-commit install
```

Fallback without `uv`:

```bash
git clone git@github.com:castorini/<repo>.git
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd <repo>
pip install -e ".[<default-extras-pip>]"
pip install <dev-tools>
<cli> doctor --output json
pre-commit install
```

For repos without optional extras, use `uv sync --group dev` and `pip install -e .`.

## Repo Parameters

| Repo | CLI | Default extras (`uv`) | Default extras (`pip`) | Dev tools |
|------|-----|------------------------|------------------------|-----------|
| `nuggetizer` | `nuggetizer` | none | none | `pre-commit pytest mypy ruff` |
| `ragnarok` | `ragnarok` | `--extra cloud --extra api` | `cloud,api` | `pre-commit pytest` |
| `rank_llm` | `rank-llm` | `--extra cloud --extra api` | `cloud,api` | `pre-commit pytest ruff` |
| `umbrela` | `umbrela` | `--extra cloud --extra hf` | `cloud,hf` | `pre-commit pytest mypy ruff` |

## Concrete Examples

### nuggetizer

```bash
git clone git@github.com:castorini/nuggetizer.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd nuggetizer
uv sync --group dev
nuggetizer doctor --output json
pre-commit install
```

### ragnarok

```bash
git clone git@github.com:castorini/ragnarok.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd ragnarok
uv sync --group dev --extra cloud --extra api
ragnarok doctor --output json
pre-commit install
```

### rank_llm

```bash
git clone git@github.com:castorini/rank_llm.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd rank_llm
uv sync --group dev --extra cloud --extra api
rank-llm doctor --output json
pre-commit install
```

### umbrela

```bash
git clone git@github.com:castorini/umbrela.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd umbrela
uv sync --group dev --extra cloud --extra hf
umbrela doctor --output json
pre-commit install
```
