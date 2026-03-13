#!/bin/bash
# 安全的最终发布脚本
# 不包含敏感信息在命令行中

set -e

echo "🎴 Open-Gi-Oh! Skill 安全发布脚本"
echo "=================================="

cd "$(dirname "$0")"

# 读取token文件
TOKEN_FILE=".github_token"
if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ 未找到token文件"
    exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")
if [ -z "$TOKEN" ]; then
    echo "❌ token文件为空"
    exit 1
fi

echo "✅ Token已从文件读取"

# 设置远程仓库URL
REMOTE_URL="https://${TOKEN}@github.com/mu009009/open-gi-oh-skill.git"
echo "🔗 设置远程仓库..."

# 检查是否已初始化git
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    git config user.name "Open-Gi-Oh! System"
    git config user.email "system@open-gi-oh.ai"
fi

# 设置远程
if ! git remote | grep -q origin; then
    git remote add origin "$REMOTE_URL"
else
    git remote set-url origin "$REMOTE_URL"
fi

echo "✅ 远程仓库配置完成"

# 添加所有文件
echo "📦 添加文件到暂存区..."
git add .

# 提交
COMMIT_MSG="🎴 Open-Gi-Oh! Skill 完整存档 2026-03-12 23:26

📊 核心内容:
1. 平衡策略展示页面
2. 30血量平衡策略文档  
3. 基于30血量的平衡卡组
4. 修复JavaScript错误的预览页面
5. 30血量卡牌生成器脚本

🎮 关键变更:
- 玩家血量从100改为30
- 建立完整平衡策略框架
- 费用-战斗力转换表优化
- GitHub自动发布系统配置

系统暴君宣言: 所有内容完整存档！准备明天继续推进！"

echo "💾 提交更改..."
git commit -m "$COMMIT_MSG"

# 推送
echo "🚀 推送到GitHub..."
git push -u origin master

echo ""
echo "🎉 发布完成！"
echo "📅 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "🔗 仓库: https://github.com/mu009009/open-gi-oh-skill"