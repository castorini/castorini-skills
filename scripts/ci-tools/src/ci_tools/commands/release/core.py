"""Pure release logic without Typer imports."""
from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Protocol

from pydantic import ValidationError

from ci_tools.commands.release.models import (
    ReleaseManifest,
    TagCheckResult,
    VersionFileError,
)

CHANGELOG_HEADING_RE = re.compile(
    r"^## v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", re.MULTILINE
)
PYPROJECT_VERSION_RE = re.compile(
    r'^(?P<prefix>version\s*=\s*")(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*))(?P<suffix>")$',
    re.MULTILINE,
)


def _load_json(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"{path} does not exist")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} contains invalid JSON: {exc}") from exc


def read_manifest(path: Path) -> ReleaseManifest:
    data = _load_json(path)
    try:
        return ReleaseManifest.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"{path}: invalid manifest - {exc}") from exc


def extract_changelog_entry(changelog: Path, version: str) -> str:
    if not changelog.is_file():
        raise ValueError(f"{changelog} does not exist")

    heading_re = re.compile(rf"^## v?{re.escape(version)}\b", re.MULTILINE)
    lines = changelog.read_text().splitlines(keepends=True)
    start_idx: int | None = None
    for idx, line in enumerate(lines):
        if heading_re.match(line):
            start_idx = idx + 1
            break

    if start_idx is None:
        raise ValueError(f"{changelog}: no entry for version {version}")

    end_idx = len(lines)
    for idx in range(start_idx, len(lines)):
        if CHANGELOG_HEADING_RE.match(lines[idx]):
            end_idx = idx
            break

    body = "".join(lines[start_idx:end_idx]).strip()
    if not body:
        raise ValueError(f"{changelog}: changelog entry for {version} is empty")
    return body


class TagsProvider(Protocol):
    """Protocol for existing tag sources."""

    def get_tags(self) -> set[str]: ...


class FileTagsProvider:
    """Read existing tags from a plain-text file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def get_tags(self) -> set[str]:
        if not self.path.is_file():
            return set()
        return {
            line.strip()
            for line in self.path.read_text().splitlines()
            if line.strip()
        }


def check_tags(provider: TagsProvider, tag: str, initial_version: str | None) -> TagCheckResult:
    existing = provider.get_tags()
    tag_error: str | None = None
    if tag in existing:
        tag_error = f"tag {tag} already exists"

    initial_version_error: str | None = None
    if initial_version and not existing:
        expected = initial_version if initial_version.startswith("v") else f"v{initial_version}"
        if tag != expected:
            initial_version_error = f"expected {expected} for first release, got {tag}"

    return TagCheckResult(
        tag_error=tag_error,
        initial_version_error=initial_version_error,
    )


def read_pyproject_version(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"{path} does not exist")
    try:
        data = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"{path} contains invalid TOML: {exc}") from exc

    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{path} does not define project.version")
    return version


def update_pyproject_version(path: Path, version: str) -> bool:
    if not path.is_file():
        raise ValueError(f"{path} does not exist")

    original = path.read_text()
    def _replace(match: re.Match[str]) -> str:
        return f'{match.group("prefix")}{version}{match.group("suffix")}'

    updated, count = PYPROJECT_VERSION_RE.subn(_replace, original, count=1)
    if count == 0:
        raise ValueError(f"{path} does not contain a project version assignment")
    if updated == original:
        return False
    path.write_text(updated)
    return True


def check_version_files(version: str, pyproject: Path | None) -> list[VersionFileError]:
    errors: list[VersionFileError] = []
    if pyproject is not None:
        current = read_pyproject_version(pyproject)
        if current != version:
            errors.append(
                VersionFileError(
                    filename=str(pyproject),
                    message=f"expected {version}, found {current}",
                )
            )
    return errors
