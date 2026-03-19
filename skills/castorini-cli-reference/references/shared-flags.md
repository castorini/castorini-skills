# Shared CLI Flags

Flags that appear identically across nuggetizer, ragnarok, and umbrela.

## Universal Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--version` | flag | — | Print package version and exit |
| `--quiet` / `-q` | flag | — | Suppress log output (stderr) |

## Output Control

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--output` | `text\|json\|jsonl` | `text` | Output format for stdout |
| `--output-file <path>` | string | — | Write primary output to file |
| `--manifest-path <path>` | string | — | Write JSON envelope to separate file |

## Write Policies (mutually exclusive)

| Flag | Description |
|------|-------------|
| `--resume` | Append to existing output file; skip already-processed records |
| `--overwrite` | Truncate existing output file before writing |
| `--fail-if-exists` | Fail immediately if output file already exists |

Default (none specified): fail if file exists.

## Validation and Dry-Run

| Flag | Description |
|------|-------------|
| `--dry-run` | Resolve inputs and report what would happen; no model calls |
| `--validate-only` | Validate declared contract (schemas, types) without resolving resources |

## Input Selection (mutually exclusive)

| Flag | Description |
|------|-------------|
| `--input-file <path>` | Read batch JSONL input from file |
| `--stdin` | Read one JSON payload from standard input |
| `--input-json <json>` | Pass JSON payload as CLI string argument |

## Model and Provider

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--model <name>` | string | varies | Model identifier |
| `--execution-mode` | `sync\|async` | `sync` | Execution mode |
| `--use-azure-openai` | flag | — | Use Azure OpenAI backend |
| `--use-openrouter` | flag | — | Use OpenRouter backend |
| `--reasoning-effort` | `none\|minimal\|low\|medium\|high\|xhigh` | — | Reasoning effort for supported models |

## Debugging and Tracing

| Flag | Description |
|------|-------------|
| `--include-trace` | Include prompt/response trace in output records |
| `--include-reasoning` | Include model reasoning fields in output records |
| `--redact-prompts` | Redact prompt content from trace fields |
| `--log-level <0\|1\|2>` | 0=warnings only, 1=info, 2=debug |

## Introspection Commands

These commands exist on all three repos:

```bash
<repo> describe <command> --output json    # command contract
<repo> schema <name> --output json         # JSON Schema for inputs/outputs
<repo> doctor --output json                # environment readiness
<repo> validate <target> --output json     # input validation
<repo> prompt list --output json           # available prompt templates
<repo> prompt show --output json           # show template definition
<repo> prompt render --output json         # render template with input
<repo> view <path> --output json           # inspect artifact file
```
