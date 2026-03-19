---
name: castorini-pipeline
description: Use when orchestrating a full Castorini evaluation pipeline — retrieve → rerank → generate → nuggetize → judge. Covers stage handoffs, JSONL format compatibility between repos, and end-to-end workflow coordination across ragnarok, nuggetizer, and umbrela.
---

# Castorini Pipeline

End-to-end pipeline orchestration across ragnarok, nuggetizer, and umbrela.

## Pipeline Stages

```
[1. Retrieve + Rerank]     ragnarok generate --dataset ...
         │ JSONL (cited answers)
         ▼
[2. Create Nuggets]        nuggetizer create --input-file ...
         │ JSONL (scored nuggets)
         ▼
[3. Assign Nuggets]        nuggetizer assign --contexts ... --nuggets ...
         │ JSONL (assigned nuggets)
         ▼
[4. Calculate Metrics]     nuggetizer metrics --input-file ...
         │ JSONL (per-query scores)
         ▼
[5. Judge Relevance]       umbrela evaluate --qrel ... --result-file ...
         │ Modified qrels + nDCG@10
         ▼
[Results]
```

## Reference Files

- `references/pipeline-walkthrough.md` — Complete end-to-end example with commands
- `references/stage-handoffs.md` — JSONL format compatibility between stages

## Stage Dependencies

| Stage | Tool | Input From | Output Format |
|-------|------|-----------|---------------|
| 1. Generate | ragnarok | Dataset or request JSONL | Cited answers JSONL |
| 2. Create nuggets | nuggetizer | Stage 1 output (as pool) | Scored nuggets JSONL |
| 3. Assign nuggets | nuggetizer | Stage 1 output + Stage 2 output | Assigned nuggets JSONL |
| 4. Metrics | nuggetizer | Stage 3 output | Per-query metrics JSONL |
| 5. Judge | umbrela | Retrieval run file + standard qrel | Modified qrels + nDCG@10 |

Note: Stages 2-4 (nuggetizer) and Stage 5 (umbrela) are independent evaluation paths — they measure different things:
- **Nuggetizer path** (stages 2-4): Measures answer completeness against extracted nuggets
- **Umbrela path** (stage 5): Measures retrieval quality against human relevance judgments

## Gotchas

- **Format alignment**: ragnarok output uses `topic_id`/`topic`; nuggetizer expects `qid`/`query`. The fields are compatible — nuggetizer normalizes both.
- **Nugget pool**: For `nuggetizer create`, the "pool" is the candidate passages, not the generated answers. Use the original retrieval input, not ragnarok's answer output.
- **Assign contexts**: For answer evaluation, use ragnarok's answer output as the contexts file (`--input-kind answers`). For retrieval evaluation, use the retrieval result as contexts (`--input-kind retrieval`).
- **Write policies**: Use `--resume` on long-running stages to allow restart without reprocessing.
- **Model consistency**: Document which model was used at each stage for reproducibility.
- **pyserini dependency**: Both ragnarok (dataset mode) and umbrela (evaluate) require pyserini.
