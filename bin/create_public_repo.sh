#!/bin/bash
# 🌐 创建公开仓库脚本（2026-03-05 新增）
# 用途：强制所有新仓库为公开模式（public）

set -e

echo "🎯 创建公开仓库工具"
echo "📝 使用说明：./create_public_repo.sh <github|gitee> <repo_name> [description]"

PLATFORM=$1
REPO_NAME=$2
DESCRIPTION=${3:-"AI No.1 中文测试自动化系统"}

if [ -z "$PLATFORM" ] || [ -z "$REPO_NAME" ]; then
  echo "❌ 错误：缺少参数"
  echo "用法: $0 <github|gitee> <repo_name> [description]"
  exit 1
fi

# GitHub Token
GITHUB_TOKEN="[REDACTED]"
# Gitee Token
GITEE_TOKEN="[REDACTED]"

# GitHub 创建公开仓库
if [ "$PLATFORM" = "github" ]; then
  echo "/github 创建仓库: $REPO_NAME"
  RESPONSE=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -d "{\"name\":\"$REPO_NAME\",\"description\":\"$DESCRIPTION\",\"private\":false}" \
    https://api.github.com/user/repos)
  
 .Clone_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('clone_url','N/A'))")
  echo "✅ GitHub 仓库创建成功: $CLONE_URL"
  echo "公开状态: private=false"

# Gitee 创建公开仓库（注意：API 可能受用户默认设置影响）
elif [ "$PLATFORM" = "gitee" ]; then
  echo "/gitee 创建仓库: $REPO_NAME"
  RESPONSE=$(curl -s -X POST \
    -d "name=$REPO_NAME" \
    -d "description=$DESCRIPTION" \
    -d "visibility=0" \
    "https://gitee.com/api/v5/user/repos?access_token=$GITEE_TOKEN")
  
  OWNER=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('namespace',{}).get('path','?'))")
  SSH_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ssh_url','N/A'))")
  
  echo "✅ Gitee 仓库创建成功: https://gitee.com/$OWNER/$REPO_NAME"
  echo "SSH: $SSH_URL"
  echo "⚠️ 注意: 如 Gitee 仍显示为私有，请 Web 页面手动设为公开"

else
  echo "❌ 错误: 不支持的平台 '$PLATFORM'"
  echo "支持平台: github, gitee"
  exit 1
fi

echo "✨ 仓库已创建，请立即使用: git clone <clone_url>"
