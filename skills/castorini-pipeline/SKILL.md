---
name: castorini-pipeline
description: Use when coordinating an end-to-end Castorini pipeline across rank_llm, ragnarok, nuggetizer, and umbrela, especially for stage handoffs, JSONL compatibility, retrieval-to-answer evaluation flow, or reproducing a multi-stage experiment.
metadata:
  version: 0.1.0
  visibility: public
---

# Castorini Pipeline

End-to-end pipeline orchestration across rank_llm, ragnarok, nuggetizer, and umbrela.

Use this skill to reason about handoffs between repositories, not as a substitute for repo-local verification. After each stage, inspect the actual artifacts before advancing.

`rank_llm` usually belongs before `ragnarok`: use it to retrieve and rerank candidate passages, then feed those contexts into `ragnarok` for answer generation and downstream nuggetizer evaluation.

## Pipeline Stages

```
[0. Retrieve + Rerank]     rank-llm rerank --dataset ...
         │ JSONL / TREC rerank artifacts
         ▼
[1. Generate Answers]      ragnarok generate --dataset ...
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
| 0. Retrieve + rerank | rank_llm | Dataset, request JSONL, or retrieval cache | Reranked JSONL / TREC-style run artifacts |
| 1. Generate | ragnarok | Dataset or request JSONL, often after rank_llm retrieval/rerank | Cited answers JSONL |
| 2. Create nuggets | nuggetizer | Stage 1 output (as pool) | Scored nuggets JSONL |
| 3. Assign nuggets | nuggetizer | Stage 1 output + Stage 2 output | Assigned nuggets JSONL |
| 4. Metrics | nuggetizer | Stage 3 output | Per-query metrics JSONL |
| 5. Judge | umbrela | Retrieval run file from rank_llm or another retriever + standard qrel | Modified qrels + nDCG@10 |

Note: Stages 2-4 (nuggetizer) and Stage 5 (umbrela) are independent evaluation paths — they measure different things:
- **Nuggetizer path** (stages 2-4): Measures answer completeness against extracted nuggets
- **Umbrela path** (stage 5): Measures retrieval quality against human relevance judgments

## Gotchas

- **Format alignment**: ragnarok output uses `topic_id`/`topic`; nuggetizer expects `qid`/`query`. The fields are compatible — nuggetizer normalizes both.
- **`rank_llm` comes first**: use it when the workflow starts from retrieval and reranking. It usually feeds `ragnarok` or `umbrela`, not the other way around.
- **Nugget pool**: For `nuggetizer create`, the "pool" is the candidate passages, not the generated answers. Use the original retrieval input, not ragnarok's answer output.
- **Assign contexts**: For answer evaluation, use ragnarok's answer output as the contexts file (`--input-kind answers`). For retrieval evaluation, use the retrieval result as contexts (`--input-kind retrieval`).
- **Write policies**: Use `--resume` on long-running stages to allow restart without reprocessing.
- **Model consistency**: Document which model was used at each stage for reproducibility.
- **pyserini dependency**: `rank_llm` retrieval workflows, `ragnarok` dataset mode, and `umbrela evaluate` all rely on pyserini-compatible setups.
- **Evaluation paths diverge**: Nuggetizer stages evaluate answer completeness, while umbrela evaluates retrieval relevance. Do not merge those metrics into one score without making the distinction explicit.
