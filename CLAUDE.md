# castorini-skills

This repo contains shared agent skills for cross-repo workflows in the Castorini research group.

## Structure

```
skills/
  anserini-fatjar/          # download and run the latest Anserini fatjar quickly
  castorini-cli-reference/   # shared CLI contract docs
  castorini-onboard/         # single-repo or multi-repo clone/bootstrap and environment setup
  castorini-pipeline/        # cross-repo pipeline orchestration
  castorini-release/         # PyPI/TestPyPI publish workflow
```

## Conventions

- Each skill has a `SKILL.md` with YAML frontmatter (`name`, `description`).
- The `description` field is a trigger: write "Use when..." not "This skill does...".
- Reference material goes in `references/` so agents can load it on demand instead of inlining everything into `SKILL.md`.
- Runnable helpers go in `scripts/`.
- Skills describe what to check and what flags exist. They do not railroad agents into rigid step-by-step flows.
- Skills reference per-repo instruction files such as `CLAUDE.md` or `AGENTS.md` for build, test, and lint instructions. They do not duplicate them.

## Target repos

- [nuggetizer](https://github.com/castorini/nuggetizer) — nugget creation, assignment, and evaluation
- [ragnarok](https://github.com/castorini/ragnarok) — RAG answer generation and TREC evaluation
- [rank_llm](https://github.com/castorini/rank_llm) — retrieval and LLM reranking workflows
- [umbrela](https://github.com/castorini/umbrela) — LLM-based relevance assessment (0–3 labels)
