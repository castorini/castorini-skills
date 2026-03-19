# agent-skills

Shared agent skills for cross-repo workflows in the [Castorini](https://github.com/castorini) research ecosystem.

This repository packages reusable skills that are useful across multiple Castorini repositories. It is intentionally small and curated: each shared skill should cover a repeatable cross-repo workflow or contract that would otherwise be duplicated in several codebases.

## What lives here

The shared skills in this repository live under `skills/`.

| Skill | Purpose |
|-------|---------|
| `castorini-cli-reference` | Shared CLI contract reference for nuggetizer, ragnarok, and umbrela |
| `install-all` | Development environment setup for one or more Castorini Python repos |
| `castorini-pipeline` | End-to-end retrieval, generation, nuggetization, and judging workflow coordination |
| `castorini-release` | PyPI and TestPyPI release workflow guidance for Castorini Python packages |

## Shared Skills vs Repo-Local Skills

Use this repository for skills that apply across repositories.

Use repo-local skills when the workflow is tightly coupled to one repository's code, tests, data layout, or release process. Those skills should live inside the repository that owns the workflow.

Today the shared skills complement repo-local skill sets that already ship with the Castorini repositories. For example:

- `nuggetizer` ships repo-local quickstart, verification, and evaluation skills
- `ragnarok` ships repo-local quickstart, verification, and dataset skills
- `umbrela` ships repo-local quickstart, verification, and evaluation skills

## Installation

### Claude Code `skillSources`

Add this repository as a remote skill source in Claude Code:

```json
{
  "permissions": {
    "allow": ["Bash(git clone*)"]
  },
  "skillSources": [
    "git@github.com:castorini/agent-skills.git"
  ]
}
```

### Local clone

Clone the repository locally:

```bash
git clone git@github.com:castorini/agent-skills.git
cd agent-skills
```

An installer script will be added in a follow-up change. Until then, link the skill directories you need into the agent runtime you are using.

### Manual symlink fallback

```bash
mkdir -p .claude/skills
ln -s /path/to/agent-skills/skills/castorini-cli-reference .claude/skills/castorini-cli-reference
ln -s /path/to/agent-skills/skills/install-all .claude/skills/install-all
ln -s /path/to/agent-skills/skills/castorini-pipeline .claude/skills/castorini-pipeline
ln -s /path/to/agent-skills/skills/castorini-release .claude/skills/castorini-release
```

## Updating Skills

Skills installed from a clone are copied or linked into an agent-specific directory. They do not update themselves automatically.

To pick up changes:

```bash
git pull origin main
```

Then relink or reinstall the skills you use.

## Why Selective Installation Matters

Installed skills add routing context for the agent. A larger installed set gives the model more candidate skills to consider on every request, which can increase trigger overlap and reduce precision.

Prefer installing only the shared skills you actively use in a workspace instead of installing every available skill by default.
