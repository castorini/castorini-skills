# Service Recipes

Recommended local stack:

- `127.0.0.1:8081` — Anserini retrieval
- `127.0.0.1:8082` — `rank_llm` reranking
- `127.0.0.1:8083` — `ragnarok` generation
- `127.0.0.1:8084` — `umbrela` judging
- `127.0.0.1:8085` — `nuggetizer` create or assign

Use `127.0.0.1` when the services are intended only for local composition. Use `0.0.0.0` only when the user explicitly wants remote access.

## Retrieval: Anserini

Use [$anserini-fatjar](/Users/ronak/castorini-monorepo/agent-skills/skills/anserini-fatjar/SKILL.md) to fetch the current jar and verify JDK 21 first.

Recommended stack command:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" io.anserini.api.RestServer --host 127.0.0.1 --port 8081
```

Common search route:

```text
GET /v1/{index}/search?query=...&hits=50
```

Example:

```bash
curl -sS "http://127.0.0.1:8081/v1/msmarco-v1-passage/search?query=what%20are%20the%20main%20uses%20of%20the%20python%20programming%20language&hits=50" | jq
```

## Rerank: rank_llm

Recommended OpenAI-backed server:

```bash
cd /Users/ronak/castorini-monorepo/rank_llm
uv run rank-llm serve http \
  --host 127.0.0.1 \
  --port 8082 \
  --model-path gpt-4o
```

Keep `rank_llm` in front of `ragnarok`, `nuggetizer create`, or `umbrela` when the user wants reranking.

## Generate: ragnarok

Recommended OpenAI-backed server:

```bash
cd /Users/ronak/castorini-monorepo/ragnarok
uv run ragnarok serve \
  --host 127.0.0.1 \
  --port 8083 \
  --model gpt-4o \
  --prompt-mode chatqa
```

Use `chatqa` as the safe default unless the user explicitly asks for a different prompt mode such as `ragnarok_v4`.

## Judge: umbrela

Recommended OpenAI-backed server:

```bash
cd /Users/ronak/castorini-monorepo/umbrela
uv run umbrela serve \
  --host 127.0.0.1 \
  --port 8084 \
  --backend gpt \
  --model gpt-4o
```

Enable `--include-trace --redact-prompts` only when the user wants prompt traces.

## Create And Assign: nuggetizer

Recommended OpenAI-backed server:

```bash
cd /Users/ronak/castorini-monorepo/nuggetizer
uv run nuggetizer serve \
  --host 127.0.0.1 \
  --port 8085 \
  --model gpt-4o
```

`nuggetizer serve` exposes both:

- `POST /v1/create`
- `POST /v1/assign`

Use `--creator-model` or `--scorer-model` only when the user wants asymmetric models.

## Health Checks

Check each HTTP service with:

```bash
curl -sS http://127.0.0.1:8082/healthz | jq
curl -sS http://127.0.0.1:8083/healthz | jq
curl -sS http://127.0.0.1:8084/healthz | jq
curl -sS http://127.0.0.1:8085/healthz | jq
```

Anserini `RestServer` does not expose the same FastAPI `/healthz` route, so validate it with a cheap search request instead.
