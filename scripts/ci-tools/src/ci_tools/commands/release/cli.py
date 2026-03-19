"""Typer sub-app for release commands."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from ci_tools.commands.release.core import (
    FileTagsProvider,
    check_tags,
    check_version_files,
    extract_changelog_entry,
    read_manifest,
    update_pyproject_version,
)
from ci_tools.commands.release.models import ReleaseOutput, SyncOutput, ValidationResult

release_app = typer.Typer(
    name="release",
    help="Release management commands.",
    no_args_is_help=True,
)

DEFAULT_MANIFEST = Path(".github/.release-manifest.json")
DEFAULT_CHANGELOG = Path("CHANGELOG.md")
DEFAULT_CI_TOOLS_PYPROJECT = Path("scripts/ci-tools/pyproject.toml")


def _die(message: str) -> None:
    typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(1)


@release_app.command("extract")
def extract(
    manifest: Path = typer.Option(DEFAULT_MANIFEST, "--manifest"),
    changelog: Path = typer.Option(DEFAULT_CHANGELOG, "--changelog"),
    tag_prefix: str = typer.Option("v", "--tag-prefix"),
) -> None:
    """Emit JSON with version, tag, and release notes."""
    try:
        release_manifest = read_manifest(manifest)
        notes = extract_changelog_entry(changelog, release_manifest.version)
    except ValueError as exc:
        _die(str(exc))
        return

    output = ReleaseOutput(
        version=release_manifest.version,
        tag=f"{tag_prefix}{release_manifest.version}",
        release_notes=notes,
    )
    typer.echo(output.model_dump_json(indent=2))


def _render_validation_summary(result: ValidationResult) -> str:
    def _status(ok: bool) -> str:
        return "pass" if ok else "FAIL"

    lines = [
        f"## Release Validation - {'passed' if result.passed else 'FAILED'}",
        "",
        "| Check | Status | Detail |",
        "|-------|--------|--------|",
        f"| Manifest version | pass | {result.version} |",
        f"| Tag `{result.tag}` | {_status(result.tag_check.tag_error is None)} | "
        f"{result.tag_check.tag_error or 'does not exist yet'} |",
        f"| Initial version | {_status(result.tag_check.initial_version_error is None)} | "
        f"{result.tag_check.initial_version_error or 'matches'} |",
        f"| Changelog entry | pass | {len(result.release_notes.splitlines())} lines |",
    ]

    for error in result.file_errors:
        lines.append(
            f"| Version sync ({error.filename}) | FAIL | {error.message} |"
        )

    lines.extend(["", "### Release Notes Preview", ""])
    for line in result.release_notes.splitlines():
        lines.append(f"> {line}" if line else ">")
    return "\n".join(lines)


@release_app.command("validate")
def validate(
    manifest: Path = typer.Option(DEFAULT_MANIFEST, "--manifest"),
    changelog: Path = typer.Option(DEFAULT_CHANGELOG, "--changelog"),
    pyproject: Optional[Path] = typer.Option(DEFAULT_CI_TOOLS_PYPROJECT, "--pyproject"),
    tags_file: Optional[Path] = typer.Option(None, "--tags-file"),
    initial_version: Optional[str] = typer.Option(None, "--initial-version"),
    tag_prefix: str = typer.Option("v", "--tag-prefix"),
) -> None:
    """Validate release metadata and versioned files."""
    try:
        release_manifest = read_manifest(manifest)
        notes = extract_changelog_entry(changelog, release_manifest.version)
        tag = f"{tag_prefix}{release_manifest.version}"
        tag_check = check_tags(
            FileTagsProvider(tags_file) if tags_file is not None else FileTagsProvider(Path("/dev/null")),
            tag,
            initial_version,
        )
        file_errors = check_version_files(release_manifest.version, pyproject)
    except ValueError as exc:
        _die(str(exc))
        return

    result = ValidationResult(
        version=release_manifest.version,
        tag=tag,
        release_notes=notes,
        tag_check=tag_check,
        file_errors=file_errors,
    )
    typer.echo(_render_validation_summary(result))
    if not result.passed:
        raise typer.Exit(1)


@release_app.command("sync")
def sync(
    manifest: Path = typer.Option(DEFAULT_MANIFEST, "--manifest"),
    pyproject: Optional[Path] = typer.Option(DEFAULT_CI_TOOLS_PYPROJECT, "--pyproject"),
) -> None:
    """Sync versioned files from the release manifest."""
    try:
        release_manifest = read_manifest(manifest)
    except ValueError as exc:
        _die(str(exc))
        return

    updated: list[str] = []
    if pyproject is not None:
        try:
            if update_pyproject_version(pyproject, release_manifest.version):
                updated.append(str(pyproject))
        except ValueError as exc:
            _die(str(exc))
            return

    typer.echo(json.dumps(SyncOutput(version=release_manifest.version, updated=updated).model_dump(), indent=2))
