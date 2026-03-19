---
name: castorini-cli-reference
description: Use when building, debugging, or reviewing CLI commands across nuggetizer, ragnarok, or umbrela — covers the shared castorini.cli.v1 JSON envelope, common flags, exit codes, artifact shapes, and cross-repo consistency expectations.
---

# Castorini CLI Reference

Quick reference for the shared CLI contract across the three Python Castorini repos: **nuggetizer**, **ragnarok**, and **umbrela**.

All three repos expose a repo-named binary (`nuggetizer`, `ragnarok`, `umbrela`) with converged introspection commands, JSON envelope, exit codes, and public flags.

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
- **umbrela**: `judge`, `evaluate`

## Reference Files

Read these on demand for detailed specifications:

- `references/envelope-schema.md` — Full `castorini.cli.v1` envelope specification
- `references/shared-flags.md` — Common flags across all three repos
- `references/artifact-shape.md` — Artifact metadata shape and conventions

## Gotchas

- **Flag casing**: All three repos use kebab-case for CLI flags (`--input-file`, not `--input_file`). Legacy scripts may still use snake_case internally.
- **`--output` vs `--output-file`**: `--output` controls format (`text|json|jsonl`); `--output-file` controls destination path. These are independent.
- **Write policies are mutually exclusive**: `--resume`, `--overwrite`, and `--fail-if-exists` cannot be combined.
- **`--dry-run` vs `--validate-only`**: `--dry-run` resolves inputs and reports what would happen. `--validate-only` checks the declared contract (schemas, types) without resolving resources.
- **Exit code 7** means partial success — some records succeeded, others failed. Check `errors` array in the JSON envelope.
- **No automated contract tests** yet verify sibling CLIs agree on the shared envelope. When in doubt, run `<repo> schema cli-envelope` to see the current shape.
