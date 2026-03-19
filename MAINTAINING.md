# Maintaining Shared Skills

This repository is for maintaining the existing shared Castorini skills. Keep the scope narrow: these skills should encode workflows or contracts that are reused across repositories.

## Trigger Descriptions

The `description` field in `SKILL.md` is routing text for the model. Write it as a trigger:

- say when the skill should be used
- mention the concrete repositories, commands, or workflows it covers
- avoid summary-style phrases that do not help activation

## Keep `SKILL.md` Concise

The body of each `SKILL.md` should be short enough to load cheaply.

- keep the core workflow in `SKILL.md`
- move long command catalogs, schemas, and detailed examples into `references/`
- avoid repeating information that already lives in reference files

## When to Use `references/`

Put information in `references/` when the model may need it, but only after the skill has already triggered.

Good candidates:

- command inventories
- data shape details
- step-by-step walkthroughs
- optional environment and dependency notes

## When to Use `scripts/`

Put deterministic or repetitive logic in `scripts/` instead of rewriting it in prose every time.

Good candidates:

- preflight checks
- validation helpers
- format conversion helpers
- release or packaging checks

Scripts should be small, readable, and callable directly from the repository root or skill directory without hidden setup.

## Gotchas

Every maintained shared skill should include a `Gotchas` section once there are known failure modes.

Prioritize:

- field-name mismatches between repos
- flags that are easy to confuse
- environment prerequisites
- write-policy and resume behavior
- assumptions that are true in one repository but not another

## Naming and Layout

- Keep one skill per directory under `skills/`.
- Keep the frontmatter `name` stable once published.
- Use installer-safe names: lowercase kebab-case only.
- Keep reference and script paths relative to the skill directory.

## Review Checklist

Before merging changes to an existing shared skill:

- frontmatter parses cleanly
- `description` is trigger-oriented
- any referenced file actually exists
- examples use current repository paths and commands
- the skill avoids duplicating large blocks already kept in `references/`
