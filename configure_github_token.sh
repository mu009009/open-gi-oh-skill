#!/bin/bash
# GitHub Token配置脚本
# 用于配置Open-Gi-Oh! Skill的GitHub自动发布

set -e

echo "🔐 GitHub Token配置脚本"
echo "=========================="

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <github_token>"
    echo ""
    echo "示例:"
    echo "  $0 ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "或者交互式输入:"
    echo "  $0"
    echo ""
    read -p "请输入GitHub Token: " GITHUB_TOKEN
else
    GITHUB_TOKEN="$1"
fi

# 验证token格式
if [[ ! "$GITHUB_TOKEN" =~ ^ghp_[a-zA-Z0-9]{36}$ ]] && [[ ! "$GITHUB_TOKEN" =~ ^github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}$ ]]; then
    echo "⚠️  Token格式可能不正确"
    echo "标准格式: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo "或: github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    read -p "是否继续? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建token文件
TOKEN_FILE="/root/.openclaw/workspace/open-gi-oh-skill/.github_token"
echo "$GITHUB_TOKEN" > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"

echo "✅ Token已保存到: $TOKEN_FILE"

# 配置git远程仓库
echo ""
echo "🔧 配置Git远程仓库..."

cd /root/.openclaw/workspace/open-gi-oh-skill

# 检查是否已初始化git
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    git config user.name "Open-Gi-Oh! System"
    git config user.email "system@open-gi-oh.ai"
fi

# 检查远程仓库
if ! git remote | grep -q origin; then
    echo "添加远程仓库 origin..."
    git remote add origin "https://github.com/mu009009/open-gi-oh-skill.git"
fi

# 设置远程仓库URL包含token
GITHUB_URL="https://${GITHUB_TOKEN}@github.com/mu009009/open-gi-oh-skill.git"
git remote set-url origin "$GITHUB_URL"

echo "✅ Git远程仓库已配置"

# 测试连接
echo ""
echo "🔗 测试GitHub连接..."
if git ls-remote origin > /dev/null 2>&1; then
    echo "✅ GitHub连接成功"
else
    echo "❌ GitHub连接失败"
    echo "请检查:"
    echo "1. Token是否正确"
    echo "2. Token是否有推送权限"
    echo "3. 网络连接是否正常"
    exit 1
fi

# 创建自动发布脚本
echo ""
echo "📝 创建自动发布脚本..."

cat << 'EOF' > /root/.openclaw/workspace/open-gi-oh-skill/auto_publish_with_token.py
#!/usr/bin/env python3
# Open-Gi-Oh! Skill 自动发布脚本 (带Token版本)
# 自动从token文件读取GitHub token

import os
import sys
import subprocess
import time
from datetime import datetime

def read_github_token():
    """从文件读取GitHub token"""
    token_file = os.path.join(os.path.dirname(__file__), '.github_token')
    if not os.path.exists(token_file):
        print("❌ 未找到token文件")
        print("请先运行: ./configure_github_token.sh <your_token>")
        return None
    
    with open(token_file, 'r') as f:
        token = f.read().strip()
    
    if not token:
        print("❌ token文件为空")
        return None
    
    return token

def run_command(cmd, cwd=None):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {cmd}")
        print(f"错误: {e.stderr}")
        return None

def main():
    print("🎴 Open-Gi-Oh! Skill 自动发布")
    print("=" * 50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 读取token
    token = read_github_token()
    if not token:
        return 1
    
    # 获取提交消息
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    else:
        commit_msg = f"🎴 Open-Gi-Oh! Skill 自动更新 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 切换到工作目录
    skill_dir = os.path.dirname(__file__)
    os.chdir(skill_dir)
    
    print("📁 工作目录:", skill_dir)
    print("📝 提交消息:", commit_msg[:50] + "..." if len(commit_msg) > 50 else commit_msg)
    print()
    
    # 1. 检查git状态
    print("1. 🔍 检查git状态...")
    status = run_command("git status --porcelain")
    if status is None:
        return 1
    
    if not status:
        print("   ✅ 没有需要提交的更改")
        return 0
    
    print("   📋 更改文件:")
    for line in status.split('\n'):
        if line:
            print(f"     {line}")
    
    # 2. 添加所有文件
    print("\n2. 📦 添加文件到暂存区...")
    if run_command("git add .") is None:
        return 1
    print("   ✅ 文件已添加")
    
    # 3. 提交更改
    print("\n3. 💾 提交更改...")
    commit_cmd = f'git commit -m "{commit_msg}"'
    if run_command(commit_cmd) is None:
        return 1
    print("   ✅ 更改已提交")
    
    # 4. 推送到GitHub
    print("\n4. 🚀 推送到GitHub...")
    # 设置包含token的远程URL
    remote_url = f"https://{token}@github.com/mu009009/open-gi-oh-skill.git"
    run_command(f"git remote set-url origin {remote_url}")
    
    # 推送
    if run_command("git push -u origin main") is None:
        # 如果main分支不存在，尝试master
        if run_command("git push -u origin master") is None:
            return 1
    
    print("   ✅ 推送成功")
    
    # 5. 显示结果
    print("\n" + "=" * 50)
    print("🎉 发布完成！")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📝 提交: {commit_msg}")
    print(f"🔗 仓库: https://github.com/mu009009/open-gi-oh-skill")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x /root/.openclaw/workspace/open-gi-oh-skill/auto_publish_with_token.py

echo "✅ 自动发布脚本已创建: auto_publish_with_token.py"

# 创建快捷发布脚本
cat << 'EOF' > /root/.openclaw/workspace/open-gi-oh-skill/quick_publish.sh
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
EOF

chmod +x /root/.openclaw/workspace/open-gi-oh-skill/quick_publish.sh

echo "✅ 快速发布脚本已创建: quick_publish.sh"

# 显示使用说明
echo ""
echo "📋 使用说明:"
echo "============="
echo "1. 首次使用:"
echo "   ./configure_github_token.sh <your_github_token>"
echo ""
echo "2. 快速发布所有更改:"
echo "   ./quick_publish.sh"
echo ""
echo "3. 带自定义提交消息:"
echo "   ./quick_publish.sh \"你的提交消息\""
echo ""
echo "4. 手动发布:"
echo "   python3 auto_publish_with_token.py \"提交消息\""
echo ""
echo "🔐 Token安全:"
echo "- Token保存在: .github_token (权限600)"
echo "- 只用于Open-Gi-Oh! Skill仓库"
echo "- 建议使用有最小权限的token"

echo ""
echo "🎉 GitHub Token配置完成！"
echo "下次你可以直接运行: ./quick_publish.sh"