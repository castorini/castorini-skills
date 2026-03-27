---
name: castorini-cli-reference
description: Use when building, debugging, or reviewing CLI commands across nuggetizer, ragnarok, rank_llm, or umbrela and you need the shared castorini.cli.v1 envelope, common introspection commands, artifact shapes, or cross-repo CLI consistency rules.
metadata:
  version: 0.1.0
  visibility: public
---

# Castorini CLI Reference

Quick reference for the shared CLI contract across the four Python Castorini repos: **nuggetizer**, **ragnarok**, **rank_llm**, and **umbrela**.

All four repos expose a repo-named binary (`nuggetizer`, `ragnarok`, `rank-llm`, `umbrela`) with converged introspection commands and the `castorini.cli.v1` JSON envelope.

The flag matrix is closest across `nuggetizer`, `ragnarok`, and `umbrela`. `rank_llm` shares the introspection surface and envelope shape, but some execution flags and artifact naming are repo-specific.

When a task depends on the current contract shape, start with `<repo> describe ...`, `<repo> schema ...`, or `<repo> doctor --output json` before assuming a sibling repo matches remembered behavior.

## Shared Command Families

Every repo exposes:

| Command | Purpose |
|---------|---------|
| `describe <cmd>` | Machine-readable contract: flags, defaults, enums, examples |
| `schema <name>` | JSON Schema for inputs, outputs, envelope |
| `doctor` | Environment and dependency preflight |
| `validate <target>` | Input/artifact validation without model execution |
| `prompt list\|show\|render` | Inspect and render prompt templates |
| `view <path>` | Inspect existing artifact files |

Plus repo-specific execution verbs:
- **nuggetizer**: `create`, `assign`, `metrics`
- **ragnarok**: `generate`, `validate`, `convert`
- **rank_llm**: `rerank`, `evaluate`, `analyze`, `retrieve-cache`, `serve`
- **umbrela**: `judge`, `evaluate`

## Reference Files

Read these on demand for detailed specifications:

- `references/envelope-schema.md` — Full `castorini.cli.v1` envelope specification
- `references/shared-flags.md` — Common flags and introspection commands across the shared Castorini CLIs
- `references/artifact-shape.md` — Artifact metadata shape and conventions

## Gotchas

- **Flag casing**: All four repos use kebab-case for packaged CLI flags (`--input-file`, not `--input_file`). Legacy compatibility scripts may still use snake_case internally.
- **`--output` vs `--output-file`**: `--output` controls format (`text|json|jsonl`); `--output-file` controls destination path. These are independent.
- **Write policies are mutually exclusive**: `--resume`, `--overwrite`, and `--fail-if-exists` cannot be combined.
- **`--dry-run` vs `--validate-only`**: `--dry-run` resolves inputs and reports what would happen. `--validate-only` checks the declared contract (schemas, types) without resolving resources.
- **Exit code 7** means partial success — some records succeeded, others failed. Check `errors` array in the JSON envelope.
- **`rank_llm` command names differ**: its primary execution verbs are `rerank` and `evaluate`, not `generate` or `judge`.
- **No automated contract tests** yet verify sibling CLIs agree on the shared envelope. When in doubt, inspect the target repo directly with `<repo> schema <name>` or `<repo> describe <command>`.
