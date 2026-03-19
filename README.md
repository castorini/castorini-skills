# agent-skills

Claude Code skills for cross-repo workflows in the [Castorini](https://github.com/castorini) research group ecosystem.

## What's here

| Skill | Purpose |
|-------|---------|
| `castorini-cli-reference` | Shared CLI contract (`castorini.cli.v1` envelope, shared flags, exit codes) across nuggetizer, ragnarok, and umbrela |
| `install-all` | Development environment setup and clone/bootstrap workflow for nuggetizer, ragnarok, and umbrela |
| `castorini-pipeline` | End-to-end retrieval → rerank → generate → nuggetize → judge pipeline orchestration |
| `castorini-release` | PyPI/TestPyPI publish workflow for nuggetizer, ragnarok, and umbrela |

The shared skills in this repo live under `skills/`.

## Installation

### As a Claude Code plugin

Add this repo as a skill source in your Claude Code settings:

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

### Manual (symlink into monorepo)

```bash
# From castorini-monorepo root
mkdir -p .claude/skills
ln -s /path/to/agent-skills/skills/castorini-cli-reference .claude/skills/castorini-cli-reference
ln -s /path/to/agent-skills/skills/install-all .claude/skills/install-all
ln -s /path/to/agent-skills/skills/castorini-pipeline .claude/skills/castorini-pipeline
ln -s /path/to/agent-skills/skills/castorini-release .claude/skills/castorini-release
```

## Per-repo skills

Each Castorini repo also ships its own skills in `<repo>/.claude/skills/`:

- **nuggetizer**: `nuggetizer-quickstart`, `nuggetizer-verify`, `nuggetizer-eval`
- **ragnarok**: `ragnarok-quickstart`, `ragnarok-verify`, `ragnarok-dataset`
- **umbrela**: `umbrela-quickstart`, `umbrela-verify`, `umbrela-eval`

These travel with the code — anyone who clones the repo gets the skills.
