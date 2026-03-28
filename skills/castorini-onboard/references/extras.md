# Castorini Python Repos — Optional Dependency Stacks

Use the shared install pattern first, then apply the repo-specific default extras from the table below.

## Shared Install Pattern

With `uv`:

```bash
uv sync --group dev <default-extras>
```

Without `uv`:

```bash
pip install -e ".[<default-extras-pip>]"
pip install <dev-tools>
```

## Repo Defaults

| Repo | Default extras (`uv`) | Default extras (`pip`) | Dev tools | Notes |
|------|------------------------|------------------------|-----------|-------|
| `nuggetizer` | none | none | `pre-commit pytest mypy ruff` | No optional extras. All runtime dependencies, including OpenAI, are in the base install. |
| `ragnarok` | `--extra cloud --extra api` | `cloud,api` | `pre-commit pytest` | API-based default dev setup. |
| `rank_llm` | `--extra openai --extra api` | `openai,api` | `pre-commit pytest ruff` | OpenAI-backed reranking plus serving support. |
| `umbrela` | `--extra cloud --extra api` | `cloud,api` | `pre-commit pytest mypy ruff` | Cloud default plus API serving support. |

## Recommended shared editable install

For the common multi-repo Castorini source setup, prefer:

```bash
uv pip install \
  -e './ragnarok[cloud,api]' \
  -e './nuggetizer[api]' \
  -e './umbrela[cloud,api]' \
  -e './rank_llm[openai,api]'
```

## Optional Extras by Repo

### nuggetizer

No optional extras.

### ragnarok

| Extra | Key Packages | Notes |
|-------|-------------|-------|
| `cloud` | openai, cohere, tiktoken | API-based, no GPU needed |
| `local` | vllm, torch, transformers, fschat, spacy, stanza | Large download, requires GPU |
| `api` | flask, gradio, pandas | Web API and UI serving |
| `pyserini` | pyserini | Requires Java 21 |
| `all` | Union of all above | |

### rank_llm

| Extra | Key Packages | Notes |
|-------|-------------|-------|
| `openai` | openai, python-dotenv, tiktoken | OpenAI-backed reranking support |
| `genai` | google-generativeai, python-dotenv | Gemini-backed reranking support |
| `cloud` | openai, google-generativeai, tiktoken | Aggregate of the OpenAI and Gemini stacks |
| `local` | torch, transformers | Local model inference |
| `api` | fastapi, flask, uvicorn | HTTP serving |
| `mcp` | fastmcp plus reranking extras | MCP server workflow |
| `vllm` | vllm plus local extras | vLLM-backed local inference |
| `sglang` | sglang plus local extras | SGLang backend |
| `tensorrt-llm` | tensorrt-llm plus local extras | TensorRT-LLM backend |
| `training` | accelerate, bitsandbytes, datasets, deepspeed | Finetuning workflow |
| `all` | Union of all above | Largest install footprint |

### umbrela

| Extra | Key Packages | Notes |
|-------|-------------|-------|
| `cloud` | openai, google-cloud-aiplatform, retry | API-based, no GPU needed |
| `api` | fastapi, uvicorn | HTTP serving |
| `hf` | torch, transformers, datasets | HuggingFace local inference |
| `fastchat` | fschat, torch, transformers | FastChat local inference |
| `pyserini` | pyserini | Requires Java 21 |
| `all` | Union of all above | |
