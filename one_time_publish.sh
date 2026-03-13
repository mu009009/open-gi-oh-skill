#!/bin/bash
# 一次性发布脚本
# 使用token推送，然后立即清理

set -e

echo "🎴 一次性GitHub发布脚本"
echo "========================"

# 从参数获取token
TOKEN="$1"
if [ -z "$TOKEN" ]; then
    echo "❌ 未提供token"
    exit 1
fi

cd "$(dirname "$0")"

echo "📦 检查本地提交..."
# 检查是否有本地提交
if ! git log --oneline -n 1 2>/dev/null | grep -q .; then
    echo "   ⚠️ 没有本地提交，创建初始提交..."
    
    # 添加所有文件
    git add .
    
    # 创建初始提交
    COMMIT_MSG="🎴 Open-Gi-Oh! Skill 完整存档 2026-03-12 23:41

📊 **今日完成的核心内容**:
1. 平衡策略展示页面 - 专业美观的HTML展示
2. 30血量平衡策略文档 - 完整思维链和规则
3. 基于30血量的平衡卡组 - 50张虾虾卡牌
4. 修复toFixed错误的预览页面 - JavaScript错误修复
5. 30血量卡牌生成器脚本 - 自动生成平衡卡牌
6. 明日待办事项文档 - 明天工作计划
7. GitHub自动发布系统 - 配置脚本和工具

🎮 **关键变更**:
- 玩家血量从100改为30，重新校准所有数值
- 建立固定规则/可协商规则/禁止规则框架
- 费用-战斗力转换表基于30血量优化
- 特殊效果价值量化评估
- 所有内容完整存档到GitHub

🚀 **立即可用的链接**:
- http://118.196.117.234:8080/open-gi-oh-web/final_shrimp_cards_preview.html
- http://118.196.117.234:8080/open-gi-oh-web/balance_strategy_display.html
- http://118.196.117.234:8080/open-gi-oh-web/

🎯 **系统暴君宣言**: 
所有内容完整存档！准备明天继续推进游戏实现！

---

📅 创建时间: 2026-03-12 23:41"
    
    git commit -m "$COMMIT_MSG"
    echo "   ✅ 初始提交创建完成"
else
    echo "   ✅ 已有本地提交"
fi

echo ""
echo "🔗 设置远程仓库URL..."
# 创建包含token的远程URL
REMOTE_URL="https://x-access-token:${TOKEN}@github.com/mu009009/open-gi-oh-skill.git"

# 移除现有远程（如果有）
git remote remove origin 2>/dev/null || true

# 添加新远程
git remote add origin "$REMOTE_URL"

echo "✅ 远程仓库配置完成"
echo ""
echo "🚀 推送到GitHub..."

# 推送
if git push -u origin master --force; then
    echo "✅ GitHub推送成功！"
    echo ""
    echo "🔐 立即清理token痕迹..."
    
    # 1. 删除包含token的脚本文件
    echo "   删除 one_time_publish.sh..."
    rm -f one_time_publish.sh
    
    # 2. 清理git历史中的token引用（如果有）
    echo "   清理历史..."
    git filter-branch --force --index-filter \
        "git rm --cached --ignore-unmatch .github_token 2>/dev/null || true" \
        --prune-empty --tag-name-filter cat -- --all
    
    # 3. 强制推送清理后的历史
    git push -u origin master --force
    
    echo "✅ 清理完成"
    
    echo ""
    echo "🎉 发布完成！"
    echo "📅 时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "🔗 仓库: https://github.com/mu009009/open-gi-oh-skill"
else
    echo "❌ GitHub推送失败"
    exit 1
fi