# Stage Handoff Formats

## Shared Request Format

`rank_llm`, `ragnarok`, `nuggetizer`, and `umbrela` all work with the same canonical request format at the repo boundaries where request JSON is exchanged:

```json
{
  "query": {"text": "...", "qid": "..."},
  "candidates": [
    {"doc": {"segment": "..."}, "docid": "...", "score": 0.0}
  ]
}
```

Lightweight shorthand (auto-normalized):

```json
{
  "query": "query text",
  "candidates": ["passage 1", "passage 2"]
}
```

## Stage 1 → Stage 2: ragnarok output → nuggetizer create input

ragnarok `generate` output:
```json
{
  "topic_id": "q1",
  "topic": "What is IR?",
  "references": ["d1", "d2"],
  "answer": [{"text": "...", "citations": [0, 1]}]
}
```

nuggetizer `create` needs the **original candidate pool**, not the answers:
```json
{
  "query": {"qid": "q1", "text": "What is IR?"},
  "candidates": [{"docid": "d1", "doc": {"segment": "..."}}]
}
```

Key: `nuggetizer create` extracts nuggets from **source passages**, not from generated answers.

## Stage 1 → Stage 3: ragnarok output → nuggetizer assign contexts

For answer evaluation (`--input-kind answers`):
```json
{"topic_id": "q1", "answer": [{"text": "IR is the science of..."}]}
```

ragnarok output can be adapted:
- `topic_id` maps to the query identifier
- The `answer` array of `CitedSentence` objects needs to be flattened to text

## Stage 2 → Stage 3: nuggetizer create output → nuggetizer assign nuggets

Direct pass-through — create output is the nuggets file for assign:
```json
{
  "qid": "q1",
  "query": "What is IR?",
  "nuggets": [
    {"text": "IR is the science of searching", "importance": "vital"},
    {"text": "IR uses NLP techniques", "importance": "okay"}
  ]
}
```

## Stage 3 → Stage 4: nuggetizer assign output → nuggetizer metrics input

Direct pass-through — assign output is the metrics input:
```json
{
  "qid": "q1",
  "nuggets": [
    {"text": "...", "importance": "vital", "assignment": "support"},
    {"text": "...", "importance": "okay", "assignment": "not_support"}
  ]
}
```

## Field Name Mapping

| Concept | ragnarok | nuggetizer | umbrela |
|---------|----------|------------|---------|
| Query ID | `topic_id` | `qid` | `qid` (in qrel) |
| Query text | `topic` | `query` | `query` |
| Document ID | `references[i]` | `docid` | `docid` (in qrel) |
| Passage text | `candidates[i].doc.segment` | `candidates[i].doc.segment` | `passage` |

`rank_llm`, `ragnarok`, and `nuggetizer` all auto-normalize between `topic_id`/`qid` and `topic`/`query` in their packaged CLIs.
