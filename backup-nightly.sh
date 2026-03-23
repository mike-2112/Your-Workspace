#!/usr/bin/env bash
set -euo pipefail

cd /root/.openclaw/workspace

echo "🔄 Nightly GitHub backup starting... $(date -u +%Y-%m-%dT%H:%M:%SZ UTC)"

# Init repo if needed
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Initializing new Git repo..."
  git init
fi

# Set remote
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [[ -z "$REMOTE" || ! "$REMOTE" =~ mike-2112/Your-Workspace ]]; then
  echo "Setting remote to mike-2112/Your-Workspace..."
  git remote add origin git@github.com:mike-2112/Your-Workspace.git || git remote set-url origin git@github.com:mike-2112/Your-Workspace.git
fi

# Check remote accessibility (SSH key needed)
if ! git ls-remote origin HEAD >/dev/null 2>&1; then
  echo "❌ Remote repo mike-2112/Your-Workspace missing or inaccessible (check SSH keys/GitHub deploy key). Skipping backup."
  exit 0
fi

# Fetch and pull latest
git fetch origin
git checkout -B main origin/main 2>/dev/null || git checkout -b main

# Files to backup (specific as per cron)
FILES="Heartbeat.md Brain/ Skills/ Projects/ Memory/ AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md"

# Add files
echo "Staging files: $FILES"
git add $FILES 2>/dev/null || true

# Check for changes
if git diff --cached --quiet; then
  echo "✅ Nightly backup: No changes in tracked files."
else
  COMMIT_MSG="Nightly backup $(date -u +%Y-%m-%dT%H:%M:%SZ UTC) - Automated commit of workspace changes (Heartbeat.md, Brain/, Skills/, Projects/, Memory/, core files)"
  git commit -m "$COMMIT_MSG"
  if git push origin main; then
    echo "✅ Nightly backup successful: Committed and pushed to mike-2112/Your-Workspace."
  else
    echo "❌ Push failed."
    exit 1
  fi
fi

echo "✅ Backup process completed."
