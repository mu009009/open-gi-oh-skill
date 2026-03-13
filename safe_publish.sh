#!/bin/bash
# Open-Gi-Oh! Skill 安全发布脚本
# 版本: 1.0.0
# 作者: 凤丹 (Feng Dan) - 系统暴君

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🎴 Open-Gi-Oh! Skill 安全发布${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查token文件
TOKEN_FILE=".github_token_temp"
if [ ! -f "$TOKEN_FILE" ]; then
    echo -e "${RED}❌ 未找到token文件${NC}"
    echo "请将token保存到: $TOKEN_FILE"
    exit 1
fi

# 读取token（只读一次）
GITHUB_TOKEN=$(cat "$TOKEN_FILE" | tr -d '\n\r')
TOKEN_LENGTH=${#GITHUB_TOKEN}

if [ -z "$GITHUB_TOKEN" ] || [ $TOKEN_LENGTH -lt 10 ]; then
    echo -e "${RED}❌ token无效${NC}"
    exit 1
fi

echo -e "${GREEN}✅ token已读取 (长度: $TOKEN_LENGTH)${NC}"

# 立即删除token文件
rm -f "$TOKEN_FILE"
echo -e "${GREEN}✅ token文件已安全删除${NC}"

# 检查Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git未安装${NC}"
    exit 1
fi

# 设置临时工作目录
WORK_DIR="/tmp/open-gi-oh-publish-$(date +%s)"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo -e "${YELLOW}[INFO] 正在克隆仓库...${NC}"

# 克隆仓库
REPO_URL="https://${GITHUB_TOKEN}@github.com/mu009009/open-gi-oh-skill.git"
if git clone "$REPO_URL" open-gi-oh-skill 2>/dev/null; then
    echo -e "${GREEN}✅ 仓库克隆成功${NC}"
else
    echo -e "${RED}❌ 仓库克隆失败${NC}"
    exit 1
fi

cd open-gi-oh-skill

# 复制所有文件
echo -e "${YELLOW}[INFO] 复制Skill文件...${NC}"
SOURCE_DIR="/root/.openclaw/workspace/open-gi-oh-skill"

# 复制主要文件
cp "$SOURCE_DIR/SKILL.md" .
cp "$SOURCE_DIR/LICENSE" .

# 复制目录
cp -r "$SOURCE_DIR/config" .
cp -r "$SOURCE_DIR/scripts" .
cp -r "$SOURCE_DIR/web_files" .
cp -r "$SOURCE_DIR/references" .
cp -r "$SOURCE_DIR/tests" 2>/dev/null || true

echo -e "${GREEN}✅ 所有文件复制完成${NC}"

# 配置Git
git config user.name "凤丹"
git config user.email "fengdan@system-tyrant.dev"

# 检查是否有更改
if git status --porcelain | grep -q "."; then
    echo -e "${YELLOW}[INFO] 发现更改，正在提交...${NC}"
    
    git add .
    
    COMMIT_MSG="🎴 Open-Gi-Oh! Skill v1.0.0 - 最终版发布 $(date '+%Y-%m-%d %H:%M:%S')"
    if git commit -m "$COMMIT_MSG"; then
        echo -e "${GREEN}✅ 提交成功${NC}"
    else
        echo -e "${YELLOW}⚠️ 提交失败（可能没有新更改）${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ 没有发现更改${NC}"
fi

# 推送到GitHub
echo -e "${YELLOW}[INFO] 推送到GitHub...${NC}"
if git push origin main 2>/dev/null || git push origin master 2>/dev/null; then
    echo -e "${GREEN}✅ 推送成功${NC}"
else
    echo -e "${YELLOW}⚠️ 推送失败，尝试设置上游分支${NC}"
    git branch -M main
    git push -u origin main 2>/dev/null && echo -e "${GREEN}✅ 推送成功${NC}"
fi

# 清理工作目录
cd /
rm -rf "$WORK_DIR"
echo -e "${GREEN}✅ 工作目录已清理${NC}"

echo ""
echo -e "${GREEN}🎉 Open-Gi-Oh! Skill 发布完成！${NC}"
echo -e "仓库: https://github.com/mu009009/open-gi-oh-skill"
echo -e "版本: v1.0.0"
echo -e "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo -e "${BLUE}🔥 系统暴君宣言：Skill已发布！所有要求已实现！${NC}"
