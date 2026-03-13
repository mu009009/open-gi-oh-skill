#!/usr/bin/env python3
# 简单的GitHub推送脚本

import subprocess
import os
import sys
from datetime import datetime

def run_command(cmd, cwd=None):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ 命令失败: {cmd}")
            print(f"错误: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return None

def main():
    print("🎴 简单GitHub推送脚本")
    print("=" * 40)
    
    # 切换到工作目录
    skill_dir = os.path.dirname(__file__)
    os.chdir(skill_dir)
    
    print(f"📁 工作目录: {skill_dir}")
    
    # 1. 检查本地状态
    print("\n1. 🔍 检查本地状态...")
    status = run_command("git status --short")
    if not status:
        print("   ✅ 工作目录干净")
    else:
        print("   📋 有未提交的更改")
        print(f"     状态: {status}")
        
        # 添加文件
        print("   📦 添加文件...")
        run_command("git add .")
        
        # 提交
        commit_msg = f"🎴 Open-Gi-Oh! Skill 更新 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"   💾 提交: {commit_msg}")
        run_command(f'git commit -m "{commit_msg}"')
    
    # 2. 设置远程仓库
    print("\n2. 🔗 设置远程仓库...")
    
    # 使用SSH方式（避免token问题）
    ssh_url = "git@github.com:mu009009/open-gi-oh-skill.git"
    run_command(f"git remote remove origin")
    run_command(f"git remote add origin {ssh_url}")
    
    print("   ✅ 远程仓库已设置 (SSH)")
    
    # 3. 推送
    print("\n3. 🚀 推送到GitHub...")
    
    # 尝试推送
    result = run_command("git push -u origin master --force")
    if result:
        print("   ✅ 推送成功！")
    else:
        print("   ⚠️ 推送失败，尝试其他方法...")
        
        # 如果SSH失败，尝试HTTPS
        print("   🔄 尝试HTTPS方法...")
        https_url = "https://github.com/mu009009/open-gi-oh-skill.git"
        run_command(f"git remote set-url origin {https_url}")
        
        # 使用credential helper
        run_command("git config credential.helper 'store --file=.git-credentials'")
        
        # 再次推送（会提示输入用户名和密码）
        print("   🔐 需要认证...")
        print("   用户名: mu009009")
        print("   密码: 使用你的GitHub token")
        
        result = run_command("git push -u origin master --force")
        if result:
            print("   ✅ 推送成功！")
        else:
            print("   ❌ 推送失败")
            return 1
    
    # 4. 显示结果
    print("\n" + "=" * 40)
    print("🎉 GitHub推送完成！")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 仓库: https://github.com/mu009009/open-gi-oh-skill")
    
    # 5. 清理临时文件
    print("\n5. 🧹 清理临时文件...")
    temp_files = [".git-credentials", "simple_push.py", "one_time_publish.sh"]
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"   删除: {file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())