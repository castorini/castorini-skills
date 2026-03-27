# castorini.cli.v1 Envelope Schema

All four Python Castorini repos (`nuggetizer`, `ragnarok`, `rank_llm`, `umbrela`) return this JSON envelope on `--output json` for primary commands.

## Shape

```json
{
  "schema_version": "castorini.cli.v1",
  "repo": "<repo_name>",
  "command": "<command>",
  "mode": "execute | dry-run | validate",
  "status": "success | partial_success | validation_error | provider_error | runtime_error",
  "exit_code": 0,
  "inputs": {},
  "resolved": {},
  "artifacts": [],
  "validation": {},
  "metrics": {},
  "warnings": [],
  "errors": []
}
```

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Always `"castorini.cli.v1"` |
| `repo` | string | Repository name: `nuggetizer`, `ragnarok`, `rank_llm`, or `umbrela` |
| `command` | string | Subcommand that was invoked (e.g., `create`, `generate`, `judge`) |
| `mode` | string | Execution mode: `execute`, `dry-run`, or `validate` |
| `status` | string | Outcome status (see below) |
| `exit_code` | int | Shell exit code (see exit code taxonomy) |
| `inputs` | object | Caller-supplied arguments after parsing |
| `resolved` | object | Normalized resources, defaults, paths, provider/backend selection |
| `artifacts` | array | Files produced, each with `kind`, `name`, and `data` or `path` |
| `validation` | object | Preflight/validation results |
| `metrics` | object | Counts, durations, record totals, token usage |
| `warnings` | array | Non-fatal issues (strings) |
| `errors` | array | Structured failures (see error shape) |

## Status Values

| Status | Meaning |
|--------|---------|
| `success` | All records processed without error |
| `partial_success` | Some records succeeded, others failed |
| `validation_error` | Input validation failed before execution |
| `provider_error` | Backend/model/API call failed |
| `runtime_error` | Unexpected runtime failure |

## Exit Code Taxonomy

| Code | Meaning |
|------|---------|
| `0` | Success |
| `2` | Invalid arguments or schema violation |
| `3` | Missing dependency, environment, or auth prerequisite |
| `4` | Missing or unreadable input/resource |
| `5` | Validation or preflight failure |
| `6` | Execution/runtime/backend failure |
| `7` | Partial success or degraded output |

Not every repo emits every status or exit code today. `rank_llm`, for example, currently uses a smaller subset of the shared taxonomy.

## Error Shape

Each entry in the `errors` array:

```json
{
  "code": "string",
  "message": "string",
  "details": {},
  "record_id": "string|null",
  "retryable": true
}
```

## Artifact Shape

Each entry in the `artifacts` array:

```json
{
  "kind": "string",
  "name": "string",
  "path": "/absolute/path/to/file",
  "data": {}
}
```

- `kind`: artifact type (e.g., `create-output`, `judge-output`, `generate-output`, `metrics-output`)
- `name`: human-readable label
- Either `path` (file on disk) or `data` (inline payload), not both

## Manifest File

When `--manifest-path <path>` is provided, the full envelope is also written to that file path as JSON — useful for downstream automation that reads the envelope separately from stdout.
