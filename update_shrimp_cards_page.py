#!/usr/bin/env python3
"""
🎴 Open-Gi-Oh! 虾虾卡页面更新脚本
用重新评估后的数据更新HTML页面
"""

import re

def update_html_file():
    """更新HTML文件中的虾虾卡数据"""
    
    html_file = 'final_shrimp_cards_preview.html'
    
    print(f"📂 读取HTML文件: {html_file}")
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原文件
        with open(html_file + '.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 原文件已备份")
        
        # 读取新的虾虾卡数据
        with open('balanced_shrimp_cards_30hp_recalculated.js', 'r', encoding='utf-8') as f:
            new_data = f.read()
        
        # 替换原JS文件引用
        # 找到原JS引用
        js_pattern = r'<script src="balanced_shrimp_cards_30hp\.js"></script>'
        
        if re.search(js_pattern, content):
            # 替换为内联数据
            new_js_ref = '<script src="balanced_shrimp_cards_30hp_recalculated.js"></script>'
            content = re.sub(js_pattern, new_js_ref, content)
            print("✅ 已更新JS文件引用")
        else:
            print("⚠️ 未找到原JS文件引用，尝试其他方法")
            
            # 尝试查找并替换数据部分
            data_pattern = r'let\s+allCards\s*=\s*balancedShrimpCards30HP;'
            if re.search(data_pattern, content):
                content = re.sub(data_pattern, 'let allCards = balancedShrimpCards30HP;', content)
                print("✅ 已更新数据引用")
        
        # 保存更新后的文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML文件已更新: {html_file}")
        print("🎉 虾虾卡重新评估已应用到页面！")
        print("   请访问: http://118.196.117.234:8080/open-gi-oh-web/final_shrimp_cards_preview.html")
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")

if __name__ == "__main__":
    update_html_file()
