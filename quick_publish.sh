#!/bin/bash
# Open-Gi-Oh! Skill 快速发布脚本

set -e

cd "$(dirname "$0")"

# 检查token
if [ ! -f ".github_token" ]; then
    echo "❌ 未配置GitHub token"
    echo "请先运行: ./configure_github_token.sh <your_token>"
    exit 1
fi

# 运行自动发布
if [ $# -eq 0 ]; then
    python3 auto_publish_with_token.py
else
    python3 auto_publish_with_token.py "$*"
fi
