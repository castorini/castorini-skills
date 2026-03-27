# castorini-skills

`castorini-skills` is a shared agent skill library for cross-repo workflows in the [Castorini](https://github.com/castorini) research ecosystem.

This repository packages reusable skills that are useful across multiple Castorini repositories. It is intentionally small and curated: each shared skill should cover a repeatable cross-repo workflow or contract that would otherwise be duplicated in several codebases.

## What lives here

The shared skills in this repository live under `skills/`.

| Skill | Purpose |
|-------|---------|
| `anserini-fatjar` | Quick Anserini setup and smoke-test workflow via the published fatjar on Maven Central |
| `castorini-cli-reference` | Shared CLI contract reference for nuggetizer, ragnarok, rank_llm, and umbrela |
| `castorini-onboard` | Development environment setup for one or more Castorini Python repos |
| `castorini-pipeline` | End-to-end retrieval, reranking, generation, nuggetization, and judging workflow coordination |
| `castorini-release` | PyPI and TestPyPI release workflow guidance for Castorini Python packages |
| `castorini-serve` | Local HTTP serving recipes and curl/jq pipelines for Anserini, rank_llm, ragnarok, nuggetizer, and umbrela |

## Shared Skills vs Repo-Local Skills

Use this repository for skills that apply across repositories.

Use repo-local skills when the workflow is tightly coupled to one repository's code, tests, data layout, or release process. Those skills should live inside the repository that owns the workflow.

Today the shared skills complement repo-local skill sets that already ship with the Castorini repositories. For example:

- `nuggetizer` ships repo-local quickstart, verification, and evaluation skills
- `ragnarok` ships repo-local quickstart, verification, and dataset skills
- `umbrela` ships repo-local quickstart, verification, and evaluation skills

`rank_llm` also uses the shared onboarding, CLI-reference, pipeline, and release skills in this repository for cross-repo workflows.

## Installation

### Claude Code `skillSources`

Add this repository as a remote skill source in Claude Code:

```json
{
  "permissions": {
    "allow": ["Bash(git clone*)"]
  },
  "skillSources": [
    "git@github.com:castorini/castorini-skills.git"
  ]
}
```

### Local clone

Clone the repository locally:

```bash
git clone git@github.com:castorini/castorini-skills.git
cd castorini-skills
./scripts/install-skills.sh list
# Default: install into the current workspace root.
./scripts/install-skills.sh add -a claude
./scripts/install-skills.sh add -a claude-code
./scripts/install-skills.sh add -a codex
# Optional: use a supported home-directory location instead.
./scripts/install-skills.sh add --home -a claude
./scripts/install-skills.sh add --home -a claude-code
./scripts/install-skills.sh add --home -a codex
# Or install into any directory (each skill becomes a subfolder there):
./scripts/install-skills.sh add -d path/workspace/skills
```

The installer discovers skills from each `SKILL.md` file and copies them into one of three locations:

- `-a <agent>`: the default agent layout under the current workspace root
- `--home -a <agent>`: the supported home-directory layout for that agent
- `-d <path>`: an explicit custom destination

Current home-directory targets are supported for `claude-code` and `codex`. Other agents should use the default workspace-root layout or `-d`.
`claude` is accepted as an alias for `claude-code`.

For more information, see `./scripts/install-skills.sh help`.

Supported agents:

- `claude` (alias for `claude-code`)
- `claude-code`
- `codex`
- `cursor`
- `gemini-cli`
- `github-copilot`
- `windsurf`
- `cline`
- `roo`
- `opencode`

### Manual symlink fallback

```bash
mkdir -p .claude/skills
ln -s /path/to/castorini-skills/skills/anserini-fatjar .claude/skills/anserini-fatjar
ln -s /path/to/castorini-skills/skills/castorini-cli-reference .claude/skills/castorini-cli-reference
ln -s /path/to/castorini-skills/skills/castorini-onboard .claude/skills/castorini-onboard
ln -s /path/to/castorini-skills/skills/castorini-pipeline .claude/skills/castorini-pipeline
ln -s /path/to/castorini-skills/skills/castorini-release .claude/skills/castorini-release
ln -s /path/to/castorini-skills/skills/castorini-serve .claude/skills/castorini-serve
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

## Acknowledgements

This skills package was informed by publicly shared work from others building practical skill systems for coding agents.

- Thariq from Anthropic for sharing [Lessons from Building Claude Code: How We Use Skills](https://x.com/trq212/status/2033949937936085378)
- Elastic for publishing the open [elastic/agent-skills](https://github.com/elastic/agent-skills) repository
