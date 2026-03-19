#!/usr/bin/env bash
# castorini-release preflight: verify a repo is ready for PyPI publish.
#
# Usage:
#   bash preflight.sh <repo-path>
#
# Checks: clean git state, version bump, build, twine check.

set -euo pipefail

REPO_PATH="${1:?Usage: preflight.sh <repo-path>}"

# Colors (respect NO_COLOR)
if [[ -z "${NO_COLOR:-}" ]]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; NC='\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; NC=''
fi

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; FAILURES=$((FAILURES + 1)); }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

FAILURES=0

cd "$REPO_PATH"

echo "=== Preflight: $(basename "$REPO_PATH") ==="

# 1. Clean git state
echo ""
echo "--- Git State ---"
if [[ -z "$(git status --porcelain)" ]]; then
  pass "Working tree is clean"
else
  fail "Uncommitted changes detected"
  git status --short
fi

# 2. Check version
echo ""
echo "--- Version ---"
VERSION=$(python3 -c "
import tomllib
with open('pyproject.toml', 'rb') as f:
    d = tomllib.load(f)
print(d.get('project', {}).get('version', 'unknown'))
")
pass "Current version: $VERSION"

# Check against latest git tag
LATEST_TAG=$(git tag --sort=-v:refname | head -1 || echo "none")
if [[ "$LATEST_TAG" == "none" ]]; then
  warn "No existing tags found"
elif [[ "$LATEST_TAG" == "v$VERSION" || "$LATEST_TAG" == "$VERSION" ]]; then
  fail "Version $VERSION matches latest tag $LATEST_TAG — bump version first"
else
  pass "Version $VERSION differs from latest tag $LATEST_TAG"
fi

# 3. Build
echo ""
echo "--- Build ---"
rm -rf dist/
if uv build 2>&1; then
  pass "uv build succeeded"
else
  fail "uv build failed"
fi

# 4. Twine check
echo ""
echo "--- Twine Check ---"
if command -v twine &>/dev/null; then
  if twine check dist/* 2>&1; then
    pass "twine check passed"
  else
    fail "twine check failed"
  fi
else
  warn "twine not installed — skipping check (pip install twine)"
fi

# 5. List artifacts
echo ""
echo "--- Build Artifacts ---"
ls -lh dist/ 2>/dev/null || warn "No dist/ directory"

# Summary
echo ""
echo "=== Summary ==="
if [[ "$FAILURES" -eq 0 ]]; then
  pass "All preflight checks passed — ready to publish"
  exit 0
else
  fail "$FAILURES preflight check(s) failed"
  exit 1
fi
