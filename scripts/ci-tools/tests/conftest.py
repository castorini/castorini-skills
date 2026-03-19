from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def temp_release_files(tmp_path: Path) -> dict[str, Path]:
    manifest = tmp_path / ".release-manifest.json"
    manifest.write_text('{"version": "0.1.0"}\n')

    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# Changelog\n\n## v0.1.0\n\n- Initial release.\n\n## v0.0.9\n\n- Older release.\n"
    )

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "[project]\nname = \"ci-tools\"\nversion = \"0.0.1\"\nrequires-python = \">=3.11\"\n"
    )

    return {
        "manifest": manifest,
        "changelog": changelog,
        "pyproject": pyproject,
    }
