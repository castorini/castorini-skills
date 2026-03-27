# Castorini Python Repos — Optional Dependency Stacks

## nuggetizer

No optional extras. All runtime dependencies (including OpenAI) are in the base install.

Dev dependencies (via `uv sync --group dev`): mypy, pre-commit, pytest, ruff, shtab, types-PyYAML, types-requests, types-tqdm.

## ragnarok

| Extra | Key Packages | Notes |
|-------|-------------|-------|
| `cloud` | openai, cohere, tiktoken | **Default for dev setup.** API-based, no GPU needed |
| `local` | vllm, torch, transformers, fschat, spacy, stanza | Large download, requires GPU |
| `api` | flask, gradio, pandas | Web API and UI serving |
| `pyserini` | pyserini | Requires Java 21 |
| `all` | Union of all above | |

Dev dependencies (via `uv sync --group dev`): pre-commit, pytest, shtab.

Install with extras:
```bash
uv sync --group dev --extra cloud --extra api
pip install -e ".[cloud,api]"
```

## rank_llm

| Extra | Key Packages | Notes |
|-------|-------------|-------|
| `cloud` | openai, google-generativeai, tiktoken | API-backed reranking providers |
| `local` | torch, transformers | Local model inference |
| `pyserini` | pyserini, faiss-cpu, pandas | Retrieval workflows; requires Java 21 |
| `api` | fastapi, flask, uvicorn | HTTP serving |
| `mcp` | fastmcp plus reranking extras | MCP server workflow |
| `vllm` | vllm plus local extras | vLLM-backed local inference |
| `sglang` | sglang plus local extras | SGLang backend |
| `tensorrt-llm` | tensorrt-llm plus local extras | TensorRT-LLM backend |
| `training` | accelerate, bitsandbytes, datasets, deepspeed | Finetuning workflow |
| `all` | Union of all above | Largest install footprint |

Dev dependencies (via `uv sync --group dev`): pre-commit, pytest, ruff.

Install with extras:
```bash
uv sync --group dev --extra cloud --extra pyserini
pip install -e ".[cloud,pyserini]"
```

## umbrela

| Extra | Key Packages | Notes |
|-------|-------------|-------|
| `cloud` | openai, google-cloud-aiplatform, retry | **Default for dev setup.** API-based, no GPU needed |
| `hf` | torch, transformers, datasets | HuggingFace local inference |
| `fastchat` | fschat, torch, transformers | FastChat local inference |
| `pyserini` | pyserini | Requires Java 21 |
| `all` | Union of all above | |

Dev dependencies (via `uv sync --group dev`): mypy, pre-commit, pytest, ruff, shtab, types-PyYAML, types-tqdm.

Install with extras:
```bash
uv sync --group dev --extra cloud --extra hf
pip install -e ".[cloud,hf]"
```
