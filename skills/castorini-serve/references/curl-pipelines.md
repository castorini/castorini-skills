# Curl Pipelines

Use `curl -sS` for pipeline stages so network errors still surface on stderr.

Use `jq` when the user wants readable output, when a stage needs only one artifact, or when you need to join multiple envelopes for `nuggetizer assign`.

## Direct Retrieval

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| jq
```

## Retrieval -> Rerank

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8082/v1/rerank \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

This works because `rank_llm` accepts the Anserini search payload directly.

## Retrieval -> Generate

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8083/v1/generate \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

## Retrieval -> Rerank -> Generate

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8082/v1/rerank \
    -H "content-type: application/json" \
    --data-binary @- \
| curl -sS -X POST http://127.0.0.1:8083/v1/generate \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

This works because `ragnarok` unwraps the `castorini.cli.v1` envelope emitted by `rank_llm` and pulls the single `rerank-results` record out of it.

## Retrieval -> Judge

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=10" \
| curl -sS -X POST http://127.0.0.1:8084/v1/judge \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

## Retrieval -> Rerank -> Judge

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8082/v1/rerank \
    -H "content-type: application/json" \
    --data-binary @- \
| curl -sS -X POST http://127.0.0.1:8084/v1/judge \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

## Retrieval -> Create Nuggets

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8085/v1/create \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

## Retrieval -> Rerank -> Create Nuggets

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8082/v1/rerank \
    -H "content-type: application/json" \
    --data-binary @- \
| curl -sS -X POST http://127.0.0.1:8085/v1/create \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

## Full Answer-Evaluation Flow

Do not try to stream the whole answer-evaluation flow as one raw pipe. `nuggetizer assign` needs both the generation envelope and the nugget envelope at the same time.

1. Save the reranked retrieval pool.

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" \
| curl -sS -X POST http://127.0.0.1:8082/v1/rerank \
    -H "content-type: application/json" \
    --data-binary @- \
> rerank.json
```

2. Generate answers from the rerank envelope.

```bash
curl -sS -X POST http://127.0.0.1:8083/v1/generate \
  -H "content-type: application/json" \
  --data-binary @rerank.json \
> answers.json
```

3. Create nuggets from the same rerank envelope, not from `answers.json`.

```bash
curl -sS -X POST http://127.0.0.1:8085/v1/create \
  -H "content-type: application/json" \
  --data-binary @rerank.json \
> nuggets.json
```

4. Join the two envelopes and send them to `nuggetizer assign`.

```bash
jq -n \
  --argfile answer answers.json \
  --argfile nugget nuggets.json \
  '{answer_envelope: $answer, nugget_envelope: $nugget}' \
| curl -sS -X POST http://127.0.0.1:8085/v1/assign \
    -H "content-type: application/json" \
    --data-binary @- \
| jq
```

For multiple answer records sharing one nugget record set, use `answers_envelope` instead of `answer_envelope`.

## Envelope Inspection

When a downstream step needs one field instead of the entire envelope, inspect it with:

```bash
jq '.artifacts[0].data' rerank.json
jq '.artifacts[0].data' answers.json
jq '.artifacts[0].data' nuggets.json
```

Some older artifacts may store payloads under `.artifacts[0].value`; the current services accept either `data` or `value` when unwrapping a `castorini.cli.v1` envelope.
