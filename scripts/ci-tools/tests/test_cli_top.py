from __future__ import annotations

from typer.testing import CliRunner

from ci_tools.cli import app


def test_top_level_help() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "release" in result.stdout
    assert "github" in result.stdout
