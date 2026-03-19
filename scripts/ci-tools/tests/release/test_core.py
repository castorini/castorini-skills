from __future__ import annotations

from pathlib import Path

import pytest

from ci_tools.commands.release.core import (
    FileTagsProvider,
    check_tags,
    check_version_files,
    extract_changelog_entry,
    read_manifest,
    read_pyproject_version,
    update_pyproject_version,
)


def test_read_manifest(temp_release_files: dict[str, Path]) -> None:
    manifest = read_manifest(temp_release_files["manifest"])
    assert manifest.version == "0.1.0"


def test_extract_changelog_entry(temp_release_files: dict[str, Path]) -> None:
    notes = extract_changelog_entry(temp_release_files["changelog"], "0.1.0")
    assert "Initial release." in notes


def test_check_tags_first_release_mismatch() -> None:
    result = check_tags(FileTagsProvider(Path("/dev/null")), "v0.2.0", "0.1.0")
    assert result.initial_version_error == "expected v0.1.0 for first release, got v0.2.0"


def test_check_version_files_reports_mismatch(temp_release_files: dict[str, Path]) -> None:
    errors = check_version_files("0.1.0", temp_release_files["pyproject"])
    assert len(errors) == 1
    assert "expected 0.1.0, found 0.0.1" in errors[0].message


def test_update_pyproject_version(temp_release_files: dict[str, Path]) -> None:
    changed = update_pyproject_version(temp_release_files["pyproject"], "0.1.0")
    assert changed is True
    assert read_pyproject_version(temp_release_files["pyproject"]) == "0.1.0"


def test_extract_changelog_missing_entry_raises(temp_release_files: dict[str, Path]) -> None:
    with pytest.raises(ValueError):
        extract_changelog_entry(temp_release_files["changelog"], "9.9.9")
