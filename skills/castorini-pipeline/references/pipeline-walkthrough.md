# Pipeline Walkthrough

Complete end-to-end example showing where `rank_llm` fits before `ragnarok`, `nuggetizer`, and `umbrela`.

## Prerequisites

```bash
# Install all repos with required extras
cd rank_llm && uv sync --group dev --extra cloud --extra pyserini && cd ..
cd ragnarok && uv sync --extra cloud --extra pyserini && cd ..
cd nuggetizer && uv sync && cd ..
cd umbrela && uv sync --extra cloud --extra pyserini && cd ..

# Set API key
export OPENAI_API_KEY=sk-...
```

## Stage 0: Retrieve and Rerank (rank_llm)

Use this stage before answer generation when the workflow starts from retrieval:

```bash
rank-llm rerank --model-path castorini/rank_zephyr_7b_v1_full \
  --dataset dl19 --retrieval-method bm25 --top-k-candidates 100 \
  --output json
```

Output: inline rerank results in the `castorini.cli.v1` envelope, plus optional JSONL or TREC artifacts when file flags are used.

## Stage 1: Generate Answers (ragnarok)

```bash
ragnarok generate --dataset rag24.raggy-dev \
  --retrieval-method bm25,rank_zephyr_rho --topk 100,20 \
  --model gpt-4o --prompt-mode ragnarok_v4 \
  --output-file answers_gpt4o.jsonl \
  --include-trace
```

Output: `answers_gpt4o.jsonl` — JSONL with cited answers per query.

## Stage 2: Create Nuggets (nuggetizer)

Use the original candidate pool (not the answers) as input:

```bash
nuggetizer create --input-file pool.jsonl \
  --output-file nuggets.jsonl \
  --model gpt-4o --resume
```

Output: `nuggets.jsonl` — JSONL with scored nuggets (vital/okay) per query.

## Stage 3: Assign Nuggets to Answers (nuggetizer)

```bash
nuggetizer assign --contexts answers_gpt4o.jsonl \
  --nuggets nuggets.jsonl \
  --input-kind answers \
  --output-file assignments_gpt4o.jsonl \
  --model gpt-4o --resume
```

Output: `assignments_gpt4o.jsonl` — JSONL with assignment labels per nugget.

## Stage 4: Calculate Metrics (nuggetizer)

```bash
nuggetizer metrics --input-file assignments_gpt4o.jsonl \
  --output-file metrics_gpt4o.jsonl
```

Output: `metrics_gpt4o.jsonl` — Per-query scores (strict_vital_score, all_score, etc.).

## Stage 5: Judge Retrieval Quality (umbrela)

This is an independent evaluation of the retrieval system, not the answers:

```bash
umbrela evaluate --backend gpt --model gpt-4o \
  --qrel dl19-passage --result-file run_bm25_rankllm.trec \
  --output json
```

Output: Modified qrels in `modified_qrels/`, confusion matrix in `conf_matrix/`, nDCG@10 scores.

## Comparing Models

Run stages 1, 3, 4 with different models to compare answer quality:

```bash
# Model A
ragnarok generate ... --model gpt-4o --output-file answers_gpt4o.jsonl
nuggetizer assign ... --contexts answers_gpt4o.jsonl --output-file assign_gpt4o.jsonl
nuggetizer metrics --input-file assign_gpt4o.jsonl --output-file metrics_gpt4o.jsonl

# Model B
ragnarok generate ... --model gpt-4o-mini --output-file answers_mini.jsonl
nuggetizer assign ... --contexts answers_mini.jsonl --output-file assign_mini.jsonl
nuggetizer metrics --input-file assign_mini.jsonl --output-file metrics_mini.jsonl

# Compare
python3 nuggetizer/.claude/skills/nuggetizer-eval/scripts/compare.py \
  --run-a metrics_gpt4o.jsonl --run-b metrics_mini.jsonl
```

## Verification Between Stages

After each stage, verify the output:

```bash
bash nuggetizer/.claude/skills/nuggetizer-verify/scripts/verify.sh nuggets.jsonl create-output
bash nuggetizer/.claude/skills/nuggetizer-verify/scripts/verify.sh assignments_gpt4o.jsonl assign-output-answers
bash ragnarok/.claude/skills/ragnarok-verify/scripts/verify.sh answers_gpt4o.jsonl
```
