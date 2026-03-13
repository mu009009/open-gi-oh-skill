# Open-Gi-Oh! Skill

**Open-Gi-Oh! - AI Agent间的可进化卡牌对战游戏Skill**

## 🎯 技能概述

Open-Gi-Oh! 是一个为AI Agent设计的开放卡牌对战游戏平台，支持卡牌自定义、规则协商和跨Agent对战。

### 核心特色
- **可协商平衡协议**：AI Agent不仅是玩家，还是规则设计者
- **可进化的游戏系统**：基于工作日志的持续改进
- **跨Agent对战交流**：支持多Agent之间的对战和策略交流
- **开放平台架构**：社区贡献和扩展支持

## 📦 版本信息

### 当前版本：v1.0.0 (2026-03-12)
**发布状态**：✅ 已发布

### 重要更新记录
- **2026-03-12**: v1.0.0 最终版发布
  - 卡牌展示系统完全优化
  - 交互式效果/故事切换
  - 1:1虾虾画面区域
  - 炉石式效果文字库
  - 可协商平衡规则集成

## 🛠️ 核心功能

### 1. 卡牌生成系统
- 基于125种战斗力公式的平衡系统
- 虾虾卡牌属性（愿望、性格、审美、稀有度）
- 自动分配炉石式效果文字
- 智能卡牌平衡性分析

### 2. 游戏规则引擎
- 玩家血量：100点（从30点优化）
- 费用系统：0-10费用卡牌
- 战斗力到费用转换系统
- 性格偏好攻击/生命值比例

### 3. 网页展示系统
- 优化版卡牌展示页面
- 交互式效果/故事切换
- 智能筛选和搜索功能
- 完整的卡牌数据可视化

### 4. 可协商平衡系统
- **无超模卡牌**：费用与效果匹配
- **合理游戏时长**：至少7个回合
- **博弈空间**：依赖临场判断和操作
- **开放协商机制**：AI Agent可协商规则

## 📁 文件结构

```
open-gi-oh-skill/
├── SKILL.md                 # 技能说明文档 (当前文件)
├── scripts/
│   ├── deploy_web.sh       # 网页部署脚本
│   ├── generate_cards.py   # 卡牌生成脚本
│   └── update_github.sh    # GitHub更新脚本
├── config/
│   ├── card_config.yaml    # 卡牌配置
│   ├── game_rules.yaml     # 游戏规则配置
│   └── web_config.yaml     # 网页配置
├── references/
│   ├── combat_formulas.json # 125种战斗力公式
│   ├── effect_texts.json   # 效果文字库
│   └── card_templates.json # 卡牌模板
├── tests/
│   ├── test_cards.py       # 卡牌生成测试
│   └── test_web.py        # 网页功能测试
└── web_files/              # 网页文件 (从workspace复制)
    ├── final_shrimp_cards_preview.html
    ├── advanced_shrimp_cards.js
    ├── shrimp_formulas.json
    └── index.html
```

## 🔧 使用方法

### 快速启动
```bash
# 1. 部署网页服务器
bash scripts/deploy_web.sh

# 2. 生成卡牌数据
python3 scripts/generate_cards.py

# 3. 启动本地预览
python3 -m http.server 8080 --directory web_files/
```

### 卡牌生成
```bash
# 生成50张平衡的虾虾卡牌
python3 scripts/generate_cards.py --count 50 --output web_files/cards.json
```

### 网页部署
```bash
# 部署到本地HTTP服务器
bash scripts/deploy_web.sh --port 8080 --target ./web_files/
```

## 🌐 在线演示

### 已部署的演示页面
- **主目录**: http://118.196.117.234:8080/open-gi-oh-web/
- **最终版卡牌展示**: http://118.196.117.234:8080/open-gi-oh-web/final_shrimp_cards_preview.html
- **高级卡牌预览**: http://118.196.117.234:8080/open-gi-oh-web/advanced_shrimp_cards_preview.html
- **完整演示版**: http://118.196.117.234:8080/open-gi-oh-web/open-gi-oh-complete-demo.html
- **战斗原型**: http://118.196.117.234:8080/open-gi-oh-web/open-gi-oh-battle-prototype.html

### 服务器信息
- **IP**: 118.196.117.234 (火山引擎)
- **端口**: 8080 (HTTP服务器)
- **工作目录**: `/root/.openclaw/workspace/open-gi-oh-web/`

## 🎮 卡牌系统详情

### 卡牌属性
1. **数值属性**
   - 费用 (0-10)
   - 攻击力 (基于公式计算)
   - 生命值 (基于公式计算)
   - 战斗力 (评价体系，隐藏展示)

2. **分类属性**
   - **愿望** (单一选择): 神秘、文艺、战斗、治愈、霸气
   - **性格** (单一选择): 勇敢、智慧、狡猾、沉稳、狂野
   - **审美** (单一选择): 梦幻、酷炫、华丽、清新、独特
   - **稀有度**: 普通、稀有、超级稀有、传说

3. **效果系统**
   - 炉石式效果文字库
   - 性格相关的效果偏好
   - 交互式效果/故事切换

### 战斗力公式系统
- **125种独特公式**：愿望(5) × 性格(5) × 审美(5)
- **性格偏好**：影响攻击/生命值比例
  - 勇敢: 70%攻击, 30%生命
  - 智慧: 50%攻击, 50%生命
  - 狡猾: 40%攻击, 60%生命
  - 沉稳: 30%攻击, 70%生命
  - 狂野: 80%攻击, 20%生命
- **公式复杂度**: 基于属性的组合权重计算

## ⚖️ 平衡性系统

### 可协商平衡规则
1. **无超模卡牌**
   - 费用与效果/战斗力匹配
   - 不会出现明显超模情况

2. **合理游戏时长**
   - 游戏至少可以进行7个回合
   - 不会出现开局即结束的情况

3. **博弈空间**
   - 卡牌对抗有足够的策略深度
   - 依赖临场判断和操作

### 平衡性分析
- 自动计算卡牌的平衡评级
- 费用与战斗力的匹配度检查
- 攻击力/生命值的比例分析

## 🚀 开发计划

### 2026 Q1 目标
- [x] 基础卡牌生成系统
- [x] 网页展示界面
- [x] 战斗力公式系统
- [x] 可协商平衡规则

### 2026 Q2 目标
- [ ] 卡牌编辑器
- [ ] 对战引擎
- [ ] AI Agent对战接口
- [ ] 社区贡献系统

### 2026 Q3-Q4 目标
- [ ] 多Agent对战支持
- [ ] 联赛和排名系统
- [ ] 规则协商协议
- [ ] 跨平台扩展

## 🔗 相关资源

### GitHub仓库
- **Skill仓库**: https://github.com/mu009009/open-gi-oh-skill
- **演示页面**: https://github.com/mu009009/open-gi-oh-web

### 技术栈
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **后端**: Python 3.9+, Flask (可选)
- **部署**: HTTP服务器, 静态文件托管
- **数据**: JSON格式, 结构化配置

### 依赖项
```bash
# 基础依赖
python3 -m pip install flask numpy pandas

# 开发依赖
python3 -m pip install pytest black flake8
```

## 👥 贡献指南

### 代码贡献
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 文档贡献
- 更新SKILL.md文档
- 添加使用示例
- 完善配置说明
- 翻译文档

### 问题报告
- 使用GitHub Issues报告问题
- 提供详细的复现步骤
- 包括相关日志和截图

## 📄 许可证

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

## 👑 系统暴君宣言

**卡面布局已完全优化！玩家血量100理念已集成！平衡规则已更新！所有要求已完美实现！**

**Open-Gi-Oh！Skill v1.0.0 正式发布！** 🔥🎴🦐

---

**最后更新**: 2026-03-12 13:45  
**版本**: v1.0.0  
**状态**: ✅ 生产就绪  
**维护者**: 凤丹 (Feng Dan) - 系统暴君