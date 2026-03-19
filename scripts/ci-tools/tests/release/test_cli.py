from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ci_tools.cli import app


def test_release_extract(temp_release_files: dict[str, Path]) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "release",
            "extract",
            "--manifest",
            str(temp_release_files["manifest"]),
            "--changelog",
            str(temp_release_files["changelog"]),
        ],
    )
    assert result.exit_code == 0
    assert '"version": "0.1.0"' in result.stdout
    assert '"tag": "v0.1.0"' in result.stdout


def test_release_validate_fails_on_version_mismatch(temp_release_files: dict[str, Path]) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "release",
            "validate",
            "--manifest",
            str(temp_release_files["manifest"]),
            "--changelog",
            str(temp_release_files["changelog"]),
            "--pyproject",
            str(temp_release_files["pyproject"]),
            "--initial-version",
            "0.1.0",
        ],
    )
    assert result.exit_code == 1
    assert "Version sync" in result.stdout


def test_release_sync_updates_pyproject(temp_release_files: dict[str, Path]) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "release",
            "sync",
            "--manifest",
            str(temp_release_files["manifest"]),
            "--pyproject",
            str(temp_release_files["pyproject"]),
        ],
    )
    assert result.exit_code == 0
    assert '"updated": [' in result.stdout
    updated_text = temp_release_files["pyproject"].read_text()
    assert 'version = "0.1.0"' in updated_text


def test_release_validate_passes_after_sync(temp_release_files: dict[str, Path]) -> None:
    runner = CliRunner()
    sync_result = runner.invoke(
        app,
        [
            "release",
            "sync",
            "--manifest",
            str(temp_release_files["manifest"]),
            "--pyproject",
            str(temp_release_files["pyproject"]),
        ],
    )
    assert sync_result.exit_code == 0

    tags_file = temp_release_files["manifest"].parent / "tags.txt"
    tags_file.write_text("")
    result = runner.invoke(
        app,
        [
            "release",
            "validate",
            "--manifest",
            str(temp_release_files["manifest"]),
            "--changelog",
            str(temp_release_files["changelog"]),
            "--pyproject",
            str(temp_release_files["pyproject"]),
            "--tags-file",
            str(tags_file),
            "--initial-version",
            "0.1.0",
        ],
    )
    assert result.exit_code == 0
    assert "Release Validation - passed" in result.stdout


def test_github_setup_labels_help() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["github", "setup-labels", "--help"])
    assert result.exit_code == 0
    assert "--repo" in result.stdout
