#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
SCRIPT_NAME="$(basename "$0")"

die() {
  echo "Error: $*" >&2
  exit 1
}

usage() {
  cat <<EOF
$SCRIPT_NAME - install shared Castorini skills from a local clone

Usage:
  $SCRIPT_NAME list
  $SCRIPT_NAME add -a claude-code

Commands:
  list              List skills discovered from SKILL.md frontmatter
  add               Copy all shared skills into the selected agent directory

Options for add:
  -a, --agent       Target agent. Supported in this scaffold: claude-code
  -h, --help        Show this help
EOF
}

parse_name() {
  local skill_file="$1"
  awk '
    BEGIN { in_frontmatter = 0 }
    /^---$/ {
      if (in_frontmatter == 0) {
        in_frontmatter = 1
        next
      }
      exit
    }
    in_frontmatter == 1 && /^name:/ {
      sub(/^name:[[:space:]]*/, "")
      gsub(/^["'"'"'"'"'"'"'"'"']|["'"'"'"'"'"'"'"'"']$/, "")
      print
      exit
    }
  ' "$skill_file"
}

discover_skill_dirs() {
  find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort
}

list_skills() {
  local found=0
  while IFS= read -r skill_file; do
    found=1
    parse_name "$skill_file"
  done < <(discover_skill_dirs)

  if [ "$found" -eq 0 ]; then
    die "No skills found under $SKILLS_DIR"
  fi
}

agent_dir_for() {
  local agent="$1"
  case "$agent" in
    claude-code) echo "$PWD/.claude/skills" ;;
    *) die "Unsupported agent '$agent' in scaffold installer. Use claude-code." ;;
  esac
}

install_all() {
  local agent="$1"
  local target_dir
  target_dir="$(agent_dir_for "$agent")"

  mkdir -p "$target_dir"

  while IFS= read -r skill_file; do
    local skill_name
    local source_dir
    skill_name="$(parse_name "$skill_file")"
    source_dir="$(dirname "$skill_file")"

    [ -n "$skill_name" ] || die "Missing skill name in $skill_file"

    rm -rf "$target_dir/$skill_name"
    cp -R "$source_dir" "$target_dir/$skill_name"
    echo "Installed $skill_name -> $target_dir/$skill_name"
  done < <(discover_skill_dirs)
}

command="${1:-}"
if [ -z "$command" ]; then
  usage
  exit 1
fi
shift || true

case "$command" in
  list)
    list_skills
    ;;
  add)
    agent=""
    while [ "$#" -gt 0 ]; do
      case "$1" in
        -a|--agent)
          [ "$#" -ge 2 ] || die "Missing value for $1"
          agent="$2"
          shift 2
          ;;
        -h|--help)
          usage
          exit 0
          ;;
        *)
          die "Unknown argument: $1"
          ;;
      esac
    done

    [ -n "$agent" ] || die "add requires -a <agent>"
    install_all "$agent"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    die "Unknown command: $command"
    ;;
esac
