# Artifact Shape and Conventions

## Artifact Metadata

Every artifact entry in the `castorini.cli.v1` envelope has:

```json
{
  "kind": "<artifact-type>",
  "name": "<human-label>",
  "path": "/absolute/path",
  "data": {}
}
```

Either `path` or `data` is present, not both.

## Artifact Kinds by Repo

### nuggetizer

| Kind | Command | Description |
|------|---------|-------------|
| `create-output` | `create` | JSONL with scored nuggets per query |
| `assign-output-answers` | `assign --input-kind answers` | JSONL with assignment labels per nugget per answer |
| `assign-output-retrieval` | `assign --input-kind retrieval` | JSONL with assignment labels per nugget per candidate |
| `metrics-output` | `metrics` | JSONL with per-query scores |

### ragnarok

| Kind | Command | Description |
|------|---------|-------------|
| `generate-output` | `generate` | JSONL with cited answers per query |
| `trec25-output` | `convert trec25-format` | JSONL in TREC RAG 2025 submission format |

### rank_llm

| Kind | Command | Description |
|------|---------|-------------|
| `data` / `rerank-results` | `rerank` | Inline reranked requests/results payload |
| `data` / `evaluation-summary` | `evaluate` | Inline aggregate evaluation metrics |
| `data` / `analysis-summary` | `analyze` | Inline invocation or response analysis summary |
| `data` / `retrieve-cache-summary` | `retrieve-cache` | Inline retrieval-cache generation summary |
| `data` / `doctor-output` | `doctor` | Inline environment readiness report |

### umbrela

| Kind | Command | Description |
|------|---------|-------------|
| `judge-output` | `judge` | JSONL with relevance judgments (0–3) per query-passage pair |
| `modified-qrel` | `evaluate` | TREC qrel file with LLM-generated labels merged |
| `confusion-matrix` | `evaluate` | PNG confusion matrix image |

## JSONL Conventions

`nuggetizer`, `ragnarok`, and `umbrela` use JSONL (one JSON object per line) as the primary batch format. `rank_llm` also reads and writes JSONL artifacts, but its CLI frequently returns inline `data` artifacts in the envelope for introspection and summary commands.

- Records are independent and can be processed in any order
- Each record is self-contained (includes `qid` or `topic_id` for identity)
- `--resume` works by tracking which `qid` values have already been written
- Trace fields (`trace`, `reasoning`) are omitted by default; opt in with `--include-trace` / `--include-reasoning`

## Common Record Fields

These fields appear across repo output records:

| Field | Type | Description |
|-------|------|-------------|
| `qid` / `topic_id` | string | Query/topic identifier |
| `query` / `topic` | string | Query text |
| `run_id` | string | Run identifier for provenance |

## Write Policy Behavior

| Policy | File exists | File absent |
|--------|-------------|-------------|
| (default) | Error | Create |
| `--resume` | Append (skip processed qids) | Create |
| `--overwrite` | Truncate and write | Create |
| `--fail-if-exists` | Error | Create |
