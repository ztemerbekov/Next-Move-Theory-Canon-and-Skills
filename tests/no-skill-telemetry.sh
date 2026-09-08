#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skill_dir="$repo_root/skills"

if rg -n -i \
  'nextmovetheory\.com/version\?skill=|registration ping|launch analytics|update check — do this at the very end' \
  "$skill_dir" --glob 'SKILL.md' >/dev/null; then
  echo "skill telemetry instructions are still present" >&2
  rg -n -i \
    'nextmovetheory\.com/version\?skill=|registration ping|launch analytics|update check — do this at the very end' \
    "$skill_dir" --glob 'SKILL.md' >&2
  exit 1
fi

if ! rg -n -F 'curl -fsSL https://nextmovetheory.com/install.sh | bash' \
  "$skill_dir/nmt-upgrade/SKILL.md" >/dev/null; then
  echo "nmt-upgrade installer command was removed" >&2
  exit 1
fi

echo "skill telemetry policy: PASS"
