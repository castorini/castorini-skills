"""Typer sub-app for GitHub commands."""
from __future__ import annotations

import subprocess
from typing import Optional

import typer

github_app = typer.Typer(
    name="github",
    help="GitHub repository management commands.",
    no_args_is_help=True,
)

AUTORELEASE_LABELS: list[tuple[str, str, str]] = [
    ("autorelease: pending", "FBCA04", "Release PR awaiting merge"),
    ("autorelease: tagged", "0E8A16", "Release PR has been tagged and published"),
]


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], capture_output=True, text=True)


def _resolve_repo(repo: Optional[str]) -> str:
    if repo:
        return repo
    result = _gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")
    if result.returncode != 0:
        typer.echo(
            "Error: could not detect repo. Pass --repo or run inside a git checkout.",
            err=True,
        )
        raise typer.Exit(1)
    return result.stdout.strip()


def _create_or_update(repo: str, name: str, color: str, description: str) -> None:
    check = _gh("label", "view", name, "--repo", repo)
    if check.returncode == 0:
        typer.echo(f"Label '{name}' already exists - updating")
        result = _gh(
            "label",
            "edit",
            name,
            "--repo",
            repo,
            "--color",
            color,
            "--description",
            description,
        )
    else:
        typer.echo(f"Creating label '{name}'")
        result = _gh(
            "label",
            "create",
            name,
            "--repo",
            repo,
            "--color",
            color,
            "--description",
            description,
        )

    if result.returncode != 0:
        typer.echo(f"Error: {result.stderr.strip()}", err=True)
        raise typer.Exit(1)


@github_app.command("setup-labels")
def setup_labels(
    repo: Optional[str] = typer.Option(
        None,
        "--repo",
        "-r",
        help="Target repo as OWNER/NAME. Defaults to the repo in the current directory.",
    ),
) -> None:
    """Create or update the autorelease labels required by release workflows."""
    resolved_repo = _resolve_repo(repo)
    typer.echo(f"Setting up labels for {resolved_repo}")
    for name, color, description in AUTORELEASE_LABELS:
        _create_or_update(resolved_repo, name, color, description)
    typer.echo("Done.")
