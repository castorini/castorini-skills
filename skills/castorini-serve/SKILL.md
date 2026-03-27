---
name: castorini-serve
description: Use when serving Anserini retrieval together with any subset of rank_llm, ragnarok, nuggetizer, or umbrela over HTTP, especially for local port planning, direct request payload compatibility, curl or jq pipelines, or sequencing retrieval, reranking, generation, nugget creation, nugget assignment, and passage judging from an Anserini fatjar RestServer.
metadata:
  version: 0.1.0
  visibility: public
---

# Castorini Serve

Serve the Castorini stack as cooperating local HTTP services.

Treat Anserini retrieval as the entry point, then add only the downstream services the user actually needs. Prefer `gpt-4o` as the default OpenAI-backed model for `rank_llm`, `ragnarok`, `nuggetizer`, and `umbrela` unless the user explicitly asks for a different model.

## Default Stack

Use this local port layout unless the user asks for different ports:

- `8081` — Anserini `RestServer`
- `8082` — `rank_llm serve http`
- `8083` — `ragnarok serve`
- `8084` — `umbrela serve`
- `8085` — `nuggetizer serve`

## Service Selection

- Retrieval only: serve Anserini through `io.anserini.api.RestServer`.
- Retrieval + rerank: add `rank_llm`.
- Retrieval + answer generation: use Anserini -> `ragnarok`, or Anserini -> `rank_llm` -> `ragnarok`.
- Retrieval + relevance judgment: use Anserini -> `umbrela`, or Anserini -> `rank_llm` -> `umbrela`.
- Retrieval + nugget creation: use Anserini -> `nuggetizer create`, or Anserini -> `rank_llm` -> `nuggetizer create`.
- Full answer-evaluation flow: keep the original retrieval or rerank payload for `nuggetizer create`, generate answers with `ragnarok`, then join the two envelopes for `nuggetizer assign`.

## Reference Files

- `references/service-recipes.md` — startup commands, port conventions, and per-service defaults
- `references/curl-pipelines.md` — direct curl, pipe, jq, and full multi-step examples

## Gotchas

- `rank_llm` serves HTTP as `rank-llm serve http ...`, not plain `rank-llm serve ...`.
- The Anserini fatjar skill documents standalone `RestServer` on `8080`, but the shared Castorini HTTP stack uses `8081` by convention so the other services can stay on `8082` through `8085`.
- `ragnarok`, `nuggetizer create`, and `umbrela` can accept raw Anserini search payloads directly because they normalize `{query, candidates}` inputs.
- `ragnarok`, `nuggetizer create`, and `umbrela` can also accept the `castorini.cli.v1` envelope returned by `rank_llm`, so a raw pipe from `rank_llm` usually works.
- `nuggetizer create` must consume the retrieval pool, not `ragnarok` answer output.
- `nuggetizer assign` does not consume a bare `ragnarok` envelope by itself; wrap `answer_envelope` plus `nugget_envelope`, or `answers_envelope` plus `nugget_envelope`, with `jq`.
- `umbrela` judges passage relevance, not answer quality. For answer quality, use the `ragnarok` plus `nuggetizer` path instead.
