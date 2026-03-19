# agent-skills

This repo contains Claude Code skills for cross-repo workflows in the Castorini research group.

## Structure

```
skills/
  castorini-cli-reference/   # shared CLI contract docs
  castorini-install/         # repo clone/bootstrap and environment setup
  castorini-pipeline/        # cross-repo pipeline orchestration
  castorini-release/         # PyPI/TestPyPI publish workflow
```

## Conventions

- Each skill has a `SKILL.md` with YAML frontmatter (`name`, `description`).
- The `description` field is a trigger: write "Use when..." not "This skill does...".
- Reference material goes in `references/` — Claude reads it on demand, not eagerly.
- Runnable helpers go in `scripts/`.
- Skills describe what to check and what flags exist. They do not railroad Claude into rigid step-by-step flows.
- Skills reference per-repo `CLAUDE.md` files for build/test/lint instructions. They do not duplicate them.

## Target repos

- [nuggetizer](https://github.com/castorini/nuggetizer) — nugget creation, assignment, and evaluation
- [ragnarok](https://github.com/castorini/ragnarok) — RAG answer generation and TREC evaluation
- [umbrela](https://github.com/castorini/umbrela) — LLM-based relevance assessment (0–3 labels)
