#!/bin/bash
# vm-ship.sh — post-run git shipper for VM-side daily doc updates.
# Usage (as ExecStartPost, or by hand):
#   GH_TOKEN=... ./vm-ship.sh ajithvnr2001/sarvam-docs --force docs/ README.md guide_code/README.md
#   GH_TOKEN=... ./vm-ship.sh ajithvnr2001/google-cloud-docs README.md
# --force needed where the paths are gitignored (sarvam ignores docs/ by design).
# Token arrives via the unit's EnvironmentFile — it must NEVER be echoed or
# committed; all output containing the URL (push/fetch stderr) is discarded.
set -uo pipefail
REPO="$1"; shift
FORCE=""
if [ "${1:-}" = "--force" ]; then FORCE="-f"; shift; fi
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${GH_TOKEN:?GH_TOKEN not set — unit EnvironmentFile missing}"
URL="https://ajithvnr2001:${GH_TOKEN}@github.com/${REPO}.git"

git add $FORCE -- "$@" 2>/dev/null
if git diff --cached --quiet >/dev/null 2>&1; then
  echo "[ship] nothing to commit"
  exit 0
fi
git commit -m "chore: daily docs update $(date -u +%F)"

for i in 1 2 3; do
  if git push "$URL" main >/dev/null 2>&1; then
    echo "[ship] pushed $(git log --oneline -1) to ${REPO}"
    exit 0
  fi
  echo "[ship] push attempt $i rejected for ${REPO}; fetching + rebasing"
  git fetch origin main >/dev/null 2>&1
  if ! git rebase origin/main >/dev/null 2>&1; then
    # only the daily stamp files ever conflict; our copy is strictly newer
    for f in docs/_last_verified.json docs/_manifest.json; do
      if git cat-file -e "HEAD:$f" 2>/dev/null && [ -e "$f" ]; then
        git checkout --ours -- "$f" && git add -u -- "$f"
      fi
    done
    GIT_EDITOR=true git rebase --continue >/dev/null 2>&1
  fi
done
echo "[ship] FAILED after 3 attempts (manual intervention needed)"
exit 1
