#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
SCRIPT_NAME="$(basename "$0")"
YES=false
FORCE=false
AGENTS=()
TARGET_DIRS=()
SELECTED_SKILLS=()

die() {
  echo "Error: $*" >&2
  exit 1
}

usage() {
  cat <<EOF
$SCRIPT_NAME - install shared Castorini skills from a local clone

Usage:
  $SCRIPT_NAME list
  $SCRIPT_NAME add (-a <agent> | -d <path>)... [options]
  $SCRIPT_NAME help

Commands:
  list                  List skills discovered from SKILL.md frontmatter
  add                   Copy shared skills into agent layout dirs and/or custom paths
  help                  Show this help

Options for add:
  -a, --agent <agent>   Target agent. Repeatable.
  -d, --dir <path>      Install skills into this directory (skills go in subdirs).
                        Repeatable. Use instead of or in addition to -a.
  -s, --skill <name>    Install a specific skill. Repeatable.
  -f, --force           Overwrite installed skills without skipping.
  -y, --yes             Skip confirmation prompts.
  -h, --help            Show this help.

Supported agents:
  claude-code
  codex
  cursor
  gemini-cli
  github-copilot
  windsurf
  cline
  roo
  opencode
EOF
}

confirm() {
  if $YES; then
    return 0
  fi

  if [ ! -t 0 ]; then
    die "No TTY available for confirmation. Re-run with --yes."
  fi

  printf "%s [Y/n] " "$1"
  read -r answer
  case "$answer" in
    [nN]*) return 1 ;;
    *) return 0 ;;
  esac
}

parse_field() {
  local skill_file="$1"
  local field="$2"
  awk -v field="$field" '
    BEGIN { in_frontmatter = 0 }
    /^---$/ {
      if (in_frontmatter == 0) {
        in_frontmatter = 1
        next
      }
      exit
    }
    in_frontmatter == 1 && index($0, field ":") == 1 {
      sub("^" field ":[[:space:]]*", "")
      gsub(/^["'"'"'"'"'"'"'"'"']|["'"'"'"'"'"'"'"'"']$/, "")
      print
      exit
    }
  ' "$skill_file"
}

discover_skill_files() {
  find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort
}

skill_exists() {
  local target="$1"
  while IFS= read -r skill_file; do
    if [ "$(parse_field "$skill_file" "name")" = "$target" ]; then
      return 0
    fi
  done < <(discover_skill_files)
  return 1
}

agent_dir_for() {
  local agent="$1"
  case "$agent" in
    claude-code) echo "$PWD/.claude/skills" ;;
    codex|cursor|gemini-cli|github-copilot|cline|opencode) echo "$PWD/.agents/skills" ;;
    windsurf) echo "$PWD/.windsurf/skills" ;;
    roo) echo "$PWD/.roo/skills" ;;
    *)
      die "Unsupported agent '$agent'"
      ;;
  esac
}

normalize_install_dir() {
  local d="$1"
  case "$d" in
    /*) printf '%s\n' "$d" ;;
    *) printf '%s\n' "$PWD/$d" ;;
  esac
}

append_unique_target() {
  local candidate="$1"
  local existing
  for existing in "${INSTALL_TARGETS[@]}"; do
    [ "$existing" = "$candidate" ] && return
  done
  INSTALL_TARGETS+=("$candidate")
}

print_discovered_skill() {
  local skill_file="$1"
  local skill_name
  local skill_description
  skill_name="$(parse_field "$skill_file" "name")"
  skill_description="$(parse_field "$skill_file" "description")"
  if [ -n "$skill_description" ]; then
    printf "%s\t%s\n" "$skill_name" "$skill_description"
  else
    printf "%s\n" "$skill_name"
  fi
}

list_skills() {
  local found=0
  while IFS= read -r skill_file; do
    found=1
    print_discovered_skill "$skill_file"
  done < <(discover_skill_files)

  if [ "$found" -eq 0 ]; then
    die "No skills found under $SKILLS_DIR"
  fi
}

install_skill_to_target() {
  local skill_file="$1"
  local target_dir="$2"
  local skill_name
  local source_dir
  skill_name="$(parse_field "$skill_file" "name")"
  source_dir="$(dirname "$skill_file")"

  [ -n "$skill_name" ] || die "Missing skill name in $skill_file"

  if [ -e "$target_dir/$skill_name" ] && ! $FORCE; then
    echo "Skipping $skill_name in $target_dir (already exists; use --force to overwrite)"
    return
  fi

  rm -rf "$target_dir/$skill_name"
  cp -R "$source_dir" "$target_dir/$skill_name"
  echo "Installed $skill_name -> $target_dir/$skill_name"
}

should_install_skill() {
  local skill_name="$1"
  if [ "${#SELECTED_SKILLS[@]}" -eq 0 ]; then
    return 0
  fi

  local selected
  for selected in "${SELECTED_SKILLS[@]}"; do
    if [ "$selected" = "$skill_name" ]; then
      return 0
    fi
  done
  return 1
}

validate_requested_skills() {
  local requested
  for requested in "${SELECTED_SKILLS[@]}"; do
    skill_exists "$requested" || die "Unknown skill '$requested'"
  done
}

install_selected() {
  [ "${#AGENTS[@]}" -gt 0 ] || [ "${#TARGET_DIRS[@]}" -gt 0 ] ||
    die "add requires at least one -a <agent> or -d <path>"
  validate_requested_skills

  INSTALL_TARGETS=()
  local agent
  local raw_dir
  for agent in "${AGENTS[@]}"; do
    append_unique_target "$(agent_dir_for "$agent")"
  done
  for raw_dir in "${TARGET_DIRS[@]}"; do
    append_unique_target "$(normalize_install_dir "$raw_dir")"
  done

  if [ "${#SELECTED_SKILLS[@]}" -eq 0 ]; then
    confirm "Install all shared skills into: ${INSTALL_TARGETS[*]}?" || exit 0
  else
    confirm "Install selected skills into: ${INSTALL_TARGETS[*]}?" || exit 0
  fi

  local target_dir
  local skill_file
  local skill_name

  for target_dir in "${INSTALL_TARGETS[@]}"; do
    mkdir -p "$target_dir"
    while IFS= read -r skill_file; do
      skill_name="$(parse_field "$skill_file" "name")"
      if should_install_skill "$skill_name"; then
        install_skill_to_target "$skill_file" "$target_dir"
      fi
    done < <(discover_skill_files)
  done
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
    while [ "$#" -gt 0 ]; do
      case "$1" in
        -a|--agent)
          [ "$#" -ge 2 ] || die "Missing value for $1"
          AGENTS+=("$2")
          shift 2
          ;;
        -d|--dir)
          [ "$#" -ge 2 ] || die "Missing value for $1"
          TARGET_DIRS+=("$2")
          shift 2
          ;;
        -s|--skill)
          [ "$#" -ge 2 ] || die "Missing value for $1"
          SELECTED_SKILLS+=("$2")
          shift 2
          ;;
        -f|--force)
          FORCE=true
          shift
          ;;
        -y|--yes)
          YES=true
          shift
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
    install_selected
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    die "Unknown command: $command"
    ;;
esac
