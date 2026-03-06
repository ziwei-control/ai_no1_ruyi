#!/bin/bash
#mirror_gitee.sh - GitHub repo → Gitee mirror (backup/fallback)
#Usage: ./mirror_gitee.sh [github_repo_url] [gitee_repo_url]

set -e

GITHUB_URL="${1:-https://github.com/ziwei-control/ai_no1_ruyi.git}"
GITEE_URL="https://pandac0:efbd92073b1ba05aa4e8fa79bc7080a0@gitee.com/pandac0/ai_no1_ruyi.git"

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "🔄 Mirror GitHub → Gitee"
echo " Source: ${GITHUB_URL}"
echo " Target: ${GITEE_URL}"

cd "$TEMP_DIR"
git clone --mirror "${GITHUB_URL}" repo.git
cd repo.git

git config --global user.name "Spanda"
git config --global user.email "spanda@copaw.local"

# Add gitee remote (or update if exists)
git remote add gitee "${GITEE_URL}" 2>/dev/null || git remote set-url gitee "${GITEE_URL}"

echo "⚙️  Pushing to Gitee..."
git push --mirror gitee

VERSION=$(date +%Y%m%d_%H%M%S)
echo "✅ Mirror completed at ${VERSION}"
echo "🔗 https://gitee.com/pandac0/ai_no1_ruyi"
