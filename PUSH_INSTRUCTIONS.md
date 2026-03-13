# 🚀 上传到GitHub的步骤

## 方法1: 使用SSH密钥 (推荐)
```bash
# 1. 添加远程仓库
git remote add origin git@github.com:mu009009/open-gi-oh-skill.git

# 2. 推送到GitHub
git push -u origin main --force

# 3. 如果没有main分支，先创建
git branch -M main
```

## 方法2: 使用HTTPS
```bash
# 1. 添加远程仓库
git remote add origin https://github.com/mu009009/open-gi-oh-skill.git

# 2. 推送到GitHub (需要GitHub Token)
git push -u origin main --force
```

## 📋 项目信息
- **提交哈希**: $(git rev-parse --short HEAD)
- **提交时间**: $(date)
- **文件数量**: $(git ls-files | wc -l)
- **虾虾卡图**: 50张 (200×200px PNG)

## 🔗 GitHub仓库
https://github.com/mu009009/open-gi-oh-skill
