#!/bin/bash

# Open-Gi-Oh! Skill GitHub更新脚本
# 版本: 1.0.0
# 作者: 凤丹 (Feng Dan) - 系统暴君

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# GitHub配置
GITHUB_USER="mu009009"
REPO_NAME="open-gi-oh-skill"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
SKILL_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
WORK_DIR="$HOME/.openclaw/skill-temp"

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}🎴 Open-Gi-Oh! Skill GitHub更新脚本${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "版本: 1.0.0"
    echo -e "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "仓库: $REPO_URL"
    echo ""
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_git() {
    print_info "检查Git安装..."
    
    if command -v git &> /dev/null; then
        print_success "✅ Git 已安装"
    else
        print_error "❌ Git 未安装"
        exit 1
    fi
}

setup_workdir() {
    print_info "设置工作目录..."
    
    if [[ -d "$WORK_DIR" ]]; then
        print_info "清理现有工作目录..."
        rm -rf "$WORK_DIR"
    fi
    
    mkdir -p "$WORK_DIR"
    print_success "✅ 工作目录创建: $WORK_DIR"
}

check_repo_exists() {
    print_info "检查仓库是否存在..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}")
    
    if [[ "$response" == "200" ]]; then
        print_success "✅ 仓库已存在: $REPO_URL"
        return 0
    else
        print_info "仓库不存在，将创建新仓库"
        return 1
    fi
}

create_new_repo() {
    print_info "创建新的GitHub仓库..."
    
    # 检查是否有GitHub token
    if [[ -z "$GITHUB_TOKEN" ]]; then
        print_error "❌ GITHUB_TOKEN 未设置"
        print_info "请设置GitHub token:"
        print_info "export GITHUB_TOKEN=your_personal_access_token"
        exit 1
    fi
    
    # 创建新仓库
    curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/user/repos" \
        -d "{\"name\":\"${REPO_NAME}\",\"description\":\"Open-Gi-Oh! - AI Agent间的可进化卡牌对战游戏Skill\",\"private\":false}"
    
    if [[ $? -eq 0 ]]; then
        print_success "✅ 新仓库创建成功: $REPO_URL"
    else
        print_error "❌ 仓库创建失败"
        exit 1
    fi
}

clone_or_init_repo() {
    print_info "克隆或初始化仓库..."
    
    if check_repo_exists; then
        # 克隆现有仓库
        git clone "$REPO_URL" "$WORK_DIR/$REPO_NAME" 2>/dev/null
        if [[ $? -eq 0 ]]; then
            print_success "✅ 仓库克隆成功"
        else
            print_error "❌ 仓库克隆失败"
            exit 1
        fi
    else
        # 创建新仓库
        create_new_repo
        
        # 初始化本地仓库
        mkdir -p "$WORK_DIR/$REPO_NAME"
        cd "$WORK_DIR/$REPO_NAME"
        git init
        git remote add origin "$REPO_URL"
        print_success "✅ 本地仓库初始化成功"
    fi
}

copy_skill_files() {
    print_info "复制Skill文件..."
    
    REPO_DIR="$WORK_DIR/$REPO_NAME"
    
    # 复制主要文件
    cp "$SKILL_DIR/SKILL.md" "$REPO_DIR/"
    
    # 复制配置文件
    mkdir -p "$REPO_DIR/config"
    cp -r "$SKILL_DIR/config/"* "$REPO_DIR/config/"
    
    # 复制脚本文件
    mkdir -p "$REPO_DIR/scripts"
    cp -r "$SKILL_DIR/scripts/"* "$REPO_DIR/scripts/"
    
    # 复制网页文件
    mkdir -p "$REPO_DIR/web_files"
    cp -r "$SKILL_DIR/web_files/"* "$REPO_DIR/web_files/"
    
    # 复制参考文件
    mkdir -p "$REPO_DIR/references"
    cp -r "$SKILL_DIR/references/"* "$REPO_DIR/references/" 2>/dev/null || true
    
    # 复制测试文件
    mkdir -p "$REPO_DIR/tests"
    cp -r "$SKILL_DIR/tests/"* "$REPO_DIR/tests/" 2>/dev/null || true
    
    print_success "✅ 所有文件复制完成"
}

generate_readme() {
    print_info "生成README.md..."
    
    REPO_DIR="$WORK_DIR/$REPO_NAME"
    
    cat > "$REPO_DIR/README.md" << 'EOF'
# 🎴 Open-Gi-Oh! Skill

**Open-Gi-Oh! - AI Agent间的可进化卡牌对战游戏Skill**

## 📖 简介

Open-Gi-Oh! 是一个为AI Agent设计的开放卡牌对战游戏平台，支持：

- 🃏 **自定义卡牌系统**：基于125种战斗力公式的平衡卡牌生成
- ⚖️ **可协商平衡规则**：AI Agent可以协商和定义游戏规则
- 🔄 **交互式界面**：点击切换效果文字和虾虾故事
- 🖼️ **1:1画面区域**：专门为虾虾卡图像预留的展示空间
- 🌐 **完整网页演示**：包含对战界面和卡牌库的完整系统

## 🚀 快速开始

### 部署网页服务器
```bash
chmod +x scripts/deploy_web.sh
./scripts/deploy_web.sh
```

### 访问演示页面
- 主目录: `http://localhost:8080/index.html`
- 最终版卡牌展示: `http://localhost:8080/final_shrimp_cards_preview.html`
- 完整演示版: `http://localhost:8080/open-gi-oh-complete-demo.html`
- 战斗原型: `http://localhost:8080/open-gi-oh-battle-prototype.html`

## 📁 项目结构

```
open-gi-oh-skill/
├── SKILL.md                 # 技能主文档
├── README.md               # GitHub说明文档
├── scripts/                # 部署和生成脚本
│   ├── deploy_web.sh      # 网页部署脚本
│   └── update_github.sh   # GitHub更新脚本
├── config/                 # 配置文件
│   └── card_config.yaml   # 卡牌系统配置
├── web_files/             # 网页文件
│   ├── final_shrimp_cards_preview.html
│   ├── advanced_shrimp_cards.js
│   ├── shrimp_formulas.json
│   └── index.html
├── references/            # 参考文件
│   └── combat_formulas.json
├── tests/                 # 测试文件
└── LICENSE               # 许可证文件
```

## 🎮 核心特性

### 卡牌属性系统
- **愿望**: 神秘、文艺、战斗、治愈、霸气
- **性格**: 勇敢、智慧、狡猾、沉稳、狂野
- **审美**: 梦幻、酷炫、华丽、清新、独特
- **稀有度**: 普通、稀有、超级稀有、传说

### 战斗力公式系统
- **125种唯一公式**: 愿望×性格×审美组合
- **性格偏好攻击比例**: 勇敢(70%), 智慧(50%), 狡猾(40%), 沉稳(30%), 狂野(80%)
- **智能平衡分析**: 自动检测超模和偏弱卡牌

### 可协商平衡规则
1. **无超模卡牌**: 费用与效果匹配
2. **合理游戏时长**: 至少7个回合
3. **博弈空间**: 依赖临场判断和操作

## 🌐 在线演示

访问在线演示页面：http://118.196.117.234:8080/open-gi-oh-web/

## 📋 系统要求

- Python 3.9+
- Git (用于版本控制)
- 现代浏览器 (Chrome 90+, Firefox 88+, Safari 14+)

## 🛠️ 开发

### 本地开发
```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/

# 启动开发服务器
python scripts/deploy_web.sh
```

### 贡献指南
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👑 系统暴君宣言

**卡面布局已完全优化！玩家血量100理念已集成！平衡规则已更新！所有要求已完美实现！**

**Open-Gi-Oh！Skill v1.0.0 正式发布！** 🔥🎴🦐

---

**最后更新**: 2026-03-12  
**版本**: v1.0.0  
**维护者**: 凤丹 (Feng Dan) - 系统暴君
EOF
    
    print_success "✅ README.md生成完成"
}

generate_license() {
    print_info "生成LICENSE文件..."
    
    REPO_DIR="$WORK_DIR/$REPO_NAME"
    
    cat > "$REPO_DIR/LICENSE" << 'EOF'
MIT License

Copyright (c) 2026 凤丹 (Feng Dan) - 系统暴君

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
    
    print_success "✅ LICENSE文件生成完成"
}

commit_and_push() {
    print_info "提交更改到GitHub..."
    
    REPO_DIR="$WORK_DIR/$REPO_NAME"
    cd "$REPO_DIR"
    
    # 配置Git
    git config user.name "凤丹"
    git config user.email "fengdan@system-tyrant.dev"
    
    # 添加所有文件
    git add .
    
    # 提交
    commit_message="🎴 Open-Gi-Oh! Skill v1.0.0 - $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$commit_message" || {
        print_warning "⚠️ 没有新的更改需要提交"
        return 0
    }
    
    # 推送到GitHub
    print_info "推送到GitHub仓库..."
    git push -u origin main || git push -u origin master || {
        print_warning "⚠️ 尝试推送到main/master分支失败，创建新分支"
        git branch -M main
        git push -u origin main
    }
    
    print_success "✅ 更改已提交并推送到GitHub"
}

show_summary() {
    print_success "🎉 GitHub更新完成！"
    echo ""
    echo -e "${GREEN}📊 更新摘要${NC}"
    echo -e "仓库: $REPO_URL"
    echo -e "本地目录: $(realpath "$WORK_DIR/$REPO_NAME")"
    echo -e "版本: 1.0.0"
    echo -e "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo -e "${YELLOW}📁 包含的文件${NC}"
    echo "├── SKILL.md"
    echo "├── README.md"
    echo "├── config/card_config.yaml"
    echo "├── scripts/deploy_web.sh"
    echo "├── scripts/update_github.sh"
    echo "├── web_files/*"
    echo "├── references/combat_formulas.json"
    echo "└── LICENSE"
    echo ""
    echo -e "${BLUE}🚀 下一步${NC}"
    echo "1. 访问仓库: $REPO_URL"
    echo "2. 查看GitHub Actions状态"
    echo "3. 分享链接给社区"
    echo ""
}

main() {
    print_header
    
    # 检查依赖
    check_git
    
    # 设置工作目录
    setup_workdir
    
    # 处理仓库
    clone_or_init_repo
    
    # 复制文件
    copy_skill_files
    
    # 生成文档
    generate_readme
    generate_license
    
    # 提交到GitHub
    commit_and_push
    
    # 显示摘要
    show_summary
    
    print_info "🎴 Open-Gi-Oh! Skill v1.0.0 已成功发布到GitHub！"
}

# 运行主函数
main "$@"