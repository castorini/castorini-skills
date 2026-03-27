# Per-Repo Install Recipes

Use these only after the `castorini-onboard` skill has already triggered and the target repo set is known.

## nuggetizer

```bash
git clone git@github.com:castorini/nuggetizer.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd nuggetizer
uv sync --group dev
nuggetizer doctor --output json
pre-commit install
```

Fallback without `uv`:

```bash
git clone git@github.com:castorini/nuggetizer.git
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd nuggetizer
pip install -e .
pip install pre-commit pytest mypy ruff
nuggetizer doctor --output json
pre-commit install
```

## ragnarok

```bash
git clone git@github.com:castorini/ragnarok.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd ragnarok
uv sync --group dev --extra cloud
ragnarok doctor --output json
pre-commit install
```

Fallback without `uv`:

```bash
git clone git@github.com:castorini/ragnarok.git
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd ragnarok
pip install -e ".[cloud]"
pip install pre-commit pytest
ragnarok doctor --output json
pre-commit install
```

## rank_llm

```bash
git clone git@github.com:castorini/rank_llm.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd rank_llm
uv sync --group dev --extra cloud --extra pyserini
rank-llm doctor --output json
pre-commit install
```

Fallback without `uv`:

```bash
git clone git@github.com:castorini/rank_llm.git
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd rank_llm
pip install -e ".[cloud,pyserini]"
pip install pre-commit pytest ruff
rank-llm doctor --output json
pre-commit install
```

## umbrela

```bash
git clone git@github.com:castorini/umbrela.git
test -d .venv-shared || uv venv --python 3.11 .venv-shared
source .venv-shared/bin/activate
cd umbrela
uv sync --group dev --extra cloud
umbrela doctor --output json
pre-commit install
```

Fallback without `uv`:

```bash
git clone git@github.com:castorini/umbrela.git
test -d .venv-shared || python3 -m venv .venv-shared
source .venv-shared/bin/activate
cd umbrela
pip install -e ".[cloud]"
pip install pre-commit pytest mypy ruff
umbrela doctor --output json
pre-commit install
```
