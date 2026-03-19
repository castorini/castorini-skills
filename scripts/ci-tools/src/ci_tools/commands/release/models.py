"""Pydantic models for release tooling."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ReleaseManifest(BaseModel):
    """Release manifest stored under .github/."""

    version: str = Field(pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class TagCheckResult(BaseModel):
    """Result of checking for existing tags and first-release expectations."""

    tag_error: str | None = None
    initial_version_error: str | None = None


class VersionFileError(BaseModel):
    """A version mismatch in a tracked file."""

    filename: str
    message: str


class ValidationResult(BaseModel):
    """Full release validation result."""

    version: str
    tag: str
    release_notes: str
    tag_check: TagCheckResult
    file_errors: list[VersionFileError] = []

    @property
    def passed(self) -> bool:
        return (
            self.tag_check.tag_error is None
            and self.tag_check.initial_version_error is None
            and not self.file_errors
        )


class ReleaseOutput(BaseModel):
    """Output of release extract."""

    version: str
    tag: str
    release_notes: str


class SyncOutput(BaseModel):
    """Output of release sync."""

    version: str
    updated: list[str]
