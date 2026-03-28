---
name: anserini-fatjar
description: Install and run Anserini quickly by downloading the latest fatjar from the official Maven Central repo instead of building from source. Use when users want fast setup, smoke tests, or command execution without Maven project compilation.
---

# Anserini Fatjar

## Overview

Use this skill to install and run Anserini quickly by downloading the latest fatjar from Maven Central into the current working directory.

Validation note:
- Validated on 2026-03-27 against `anserini-1.7.1-fatjar.jar`
- Verified locally: fatjar download, `cacm-download` reproduction, catalog lookups, `Search` CLI, and `RestServer`

## Workflow

1. Verify runtime tools.
2. Download the latest fatjar from Maven Central.
3. Run smoke test/help command.
4. Execute target commands.

For a reusable end-to-end check of the documented workflow, run:

```bash
SKILL_DIR="/path/to/anserini-fatjar"
bash "$SKILL_DIR/scripts/verify_fatjar_workflow.sh"
```

## 1. Verify Runtime Tools

Run:

```bash
java -version
javac -version
wget --version
```

Require:

- JDK 21 available on PATH for both `java` and `javac`
- `wget` available on PATH
- Optional: `jq` available on PATH for JSON filtering commands below

Stop immediately and warn the user if prerequisites are not satisfied. In particular:

- If `java -version` or `javac -version` does not report JDK 21, do not continue.
- If `wget` is missing, do not continue with Maven Central download steps.
- If `jq` is missing, continue only when JSON filtering is unnecessary or replace those examples with an equivalent plain-text inspection.

## 2. Download Latest Fatjar

```bash
bash "skills/anserini-fatjar/scripts/fetch_latest_fatjar.sh"
```

This script probes Maven Central metadata at `https://repo1.maven.org/maven2/io/anserini/anserini/maven-metadata.xml`,
extracts the current release, and downloads `anserini-<version>-fatjar.jar` from the matching official artifact path.
At the moment, a direct example URL is:

```bash
wget https://repo1.maven.org/maven2/io/anserini/anserini/1.7.1/anserini-1.7.1-fatjar.jar
```

All subsequent commands assume the jar is available in the current working directory as `anserini-<version>-fatjar.jar`.
Resolve the filename dynamically before invoking Java:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
```

## 3. Smoke Test

Run:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" \
  io.anserini.reproduce.ReproduceFromDocumentCollection \
  --download --index --verify --search --config cacm-download
```

Treat the `cacm-download` reproduction as proof the runtime is ready. This workflow downloads the
CACM collection, builds the index, verifies index statistics, runs retrieval, and checks the
expected regression metrics from the config bundled in the jar.

For BM25, the expected scores from `cacm-download` are:

- `MAP = 0.3123`
- `P30 = 0.1942`

If the command exits successfully and the BM25 verification matches those values, the fatjar is
working correctly.

## 4. Command Execution

Run Anserini commands against the downloaded jar:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" <main-class> <args>
```

Keep all commands pinned to the same downloaded jar version unless the user asks to change versions.

## 5. Prebuilt Index Catalog

To inspect the prebuilt indexes exposed by `io.anserini.cli.PrebuiltIndexCatalog`, run:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --list
```

`--list` emits JSON in the current jar, so prefer pairing it with `--filter` and `jq` instead of
grepping raw output when you need to identify a specific index.

`msmarco-v1-passage` is a particularly common choice and should be called out when users ask about available prebuilt indexes or MS MARCO passage retrieval setup.

Recommended lookup for the standard MS MARCO V1 passage inverted index:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" \
  io.anserini.cli.PrebuiltIndexCatalog \
  --list --filter '^msmarco-v1-passage$' \
| jq '.[0] | {name, type, description, filename}'
```

Useful variants:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --help
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --list --filter 'msmarco.*passage' | jq '.[].name'
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --type flat --list
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --type inverted --list
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --type impact --list
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.PrebuiltIndexCatalog --type hnsw --list
```

## 6. Topics Catalog

To inspect the topics exposed by `io.anserini.cli.TopicsCatalog`, run:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" io.anserini.cli.TopicsCatalog --list
```

`--list` emits JSON in the current jar, so prefer pairing it with `--filter` and `jq` to locate
the exact symbol you need.

To print all topics for a specific set, run:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" io.anserini.cli.TopicsCatalog --get <set>
```

For the standard MS MARCO V1 passage queries that pair with the `msmarco-v1-passage` prebuilt
index, use `msmarco-v1-passage-dev`.

Recommended lookup:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" \
  io.anserini.cli.TopicsCatalog \
  --list --filter '^msmarco-v1-passage-dev$' \
| jq '.'
```

In the current fatjar, `--list` exposes the canonical set name as `msmarco-v1-passage-dev`.
Use `--list` first to discover the exact set name, then `--get` to inspect its contents:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" io.anserini.cli.TopicsCatalog --get msmarco-v1-passage-dev
```

## 7. Search CLI

Use `io.anserini.cli.Search` for ad hoc retrieval against either a local Lucene index path or a prebuilt index name.
In the current fatjar, exactly one of `--json` or `--trec` is required.

Recommended example using the local CACM index created by the smoke test:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" \
  io.anserini.cli.Search \
  --index indexes/lucene-inverted.cacm.download \
  --query "computer programming" \
  --json --hits 10
```

Interactive mode:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" \
  io.anserini.cli.Search \
  --index indexes/lucene-inverted.cacm.download \
  --interactive --json
```

Useful output variants:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.Search --index indexes/lucene-inverted.cacm.download --query "computer programming" --json --hits 10
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"; java -cp "$ANSERINI_JAR" io.anserini.cli.Search --index indexes/lucene-inverted.cacm.download --query "computer programming" --trec --hits 10
```

The `msmarco-v1-passage` prebuilt index remains a useful option, but it is a heavyweight example:
the catalog currently advertises a compressed download of about 2.17 GB. Prefer the local CACM
index for smoke tests and quick command validation.

## 8. REST API Server

Use `io.anserini.api.RestServer` to expose search and document lookup over HTTP.

Fatjar invocation:

```bash
ANSERINI_JAR="$(ls -1 anserini-*-fatjar.jar | sort -V | tail -n 1)"
java -cp "$ANSERINI_JAR" io.anserini.api.RestServer --host 127.0.0.1 --port 8080
```

On startup, the server prints the route shape:

```text
GET /v1/{index}/search?query=...&hits=10
GET /v1/{index}/doc/{docid}
```

If `{index}` is a filesystem path instead of a prebuilt index name, URL-encode it before sending requests.
For the local CACM index created by the smoke test, this works:

```bash
curl -sS 'http://127.0.0.1:8080/v1/indexes%2Flucene-inverted.cacm.download/search?query=computer%20programming&hits=2'
curl -sS 'http://127.0.0.1:8080/v1/indexes%2Flucene-inverted.cacm.download/doc/CACM-1771'
```

If the server cannot bind to the default port `8080`, inform the user explicitly before trying a
different port. Do not silently switch ports.

If working inside an Anserini checkout, the equivalent helper script is:

```bash
bin/run.sh io.anserini.api.RestServer --host 127.0.0.1 --port 8080
```

Sample requests against the local CACM index created by the smoke test:

```bash
curl "http://127.0.0.1:8080/v1/indexes%2Flucene-inverted.cacm.download/search?query=computer%20programming&hits=5"
curl "http://127.0.0.1:8080/v1/indexes%2Flucene-inverted.cacm.download/doc/CACM-1771"
```

The document fetch route is `/doc/{docid}`, not `/documents/{docid}`.
This REST workflow works well with local indexes created during the smoke test. In restricted
environments, binding a local port may require elevated permissions.

## Troubleshooting

- Maven metadata lookup fails: re-run `wget -qO- https://repo1.maven.org/maven2/io/anserini/anserini/maven-metadata.xml` and confirm network access to Maven Central.
- Artifact download fails: confirm the resolved version exists under `https://repo1.maven.org/maven2/io/anserini/anserini/<version>/`.
- `ClassNotFoundException`: confirm the jar filename and working directory, then recompute `ANSERINI_JAR`.
- JDK prerequisite not satisfied: require JDK 21 specifically, warn the user, and stop before running the smoke test or any Anserini command.
- `wget` missing: warn the user and stop before attempting the Maven download.
- REST server bind failure on `8080`: inform the user that the default port is blocked or already in use before proposing an alternate port.
- Java errors after JDK 21 is installed: re-run with the correct `java` and `javac` on `PATH` and confirm no older JDK is shadowing them.

## Completion Criteria

Treat setup as complete when all are true:

- `anserini-<version>-fatjar.jar` exists locally.
- `ReproduceFromDocumentCollection --download --index --verify --search --config cacm-download` executes successfully.
- BM25 verification matches `MAP = 0.3123` and `P30 = 0.1942`.
- The user can run target commands via `java -cp ...`.
