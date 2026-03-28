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

## Recommended shared editable install

Run this from the parent directory where the four repositories should live:

```bash
git clone git@github.com:castorini/ragnarok.git && \
git clone git@github.com:castorini/nuggetizer.git && \
git clone git@github.com:castorini/umbrela.git && \
git clone git@github.com:castorini/rank_llm.git && \
test -d .venv-shared || uv venv --python 3.11 .venv-shared && \
source .venv-shared/bin/activate && \
uv pip install \
  -e './ragnarok[cloud,api]' \
  -e './nuggetizer[api]' \
  -e './umbrela[cloud,api]' \
  -e './rank_llm[openai,api]'
```

Smoke tests after the shared install:

```bash
(cd ragnarok && ragnarok doctor --output json)
(cd nuggetizer && nuggetizer doctor --output json)
(cd umbrela && umbrela doctor --output json)
(cd rank_llm && rank-llm doctor --output json)
```

Then install hooks in each source checkout:

```bash
(cd ragnarok && pre-commit install)
(cd nuggetizer && pre-commit install)
(cd umbrela && pre-commit install)
(cd rank_llm && pre-commit install)
```

## Repo Parameters

| Repo | CLI | Default extras (`uv`) | Default extras (`pip`) | Dev tools |
|------|-----|------------------------|------------------------|-----------|
| `nuggetizer` | `nuggetizer` | none | none | `pre-commit pytest mypy ruff` |
| `ragnarok` | `ragnarok` | `--extra cloud --extra api` | `cloud,api` | `pre-commit pytest` |
| `rank_llm` | `rank-llm` | `--extra openai --extra api` | `openai,api` | `pre-commit pytest ruff` |
| `umbrela` | `umbrela` | `--extra cloud --extra api` | `cloud,api` | `pre-commit pytest mypy ruff` |

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
uv sync --group dev --extra openai --extra api
rank-llm doctor --output json
pre-commit install
```

### umbrela

```bash
git clone git@github.com:castorini/umbrela.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd umbrela
uv sync --group dev --extra cloud --extra api
umbrela doctor --output json
pre-commit install
```
