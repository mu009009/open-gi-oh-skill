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
