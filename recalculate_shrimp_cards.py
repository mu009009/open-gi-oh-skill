#!/usr/bin/env python3
"""
🎴 Open-Gi-Oh! 虾虾卡重新评估脚本
根据新的平衡策略重新计算50张虾虾卡的数值和费用
"""

import json
import re
import math

def load_shrimp_cards():
    """从JS文件加载虾虾卡数据"""
    
    print("📂 加载虾虾卡数据...")
    
    with open('balanced_shrimp_cards_30hp.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取JSON数组部分
    # 查找 const balancedShrimpCards30HP = [ ... ];
    match = re.search(r'const\s+balancedShrimpCards30HP\s*=\s*(\[.*?\]);', content, re.DOTALL)
    
    if not match:
        print("❌ 无法找到虾虾卡数据")
        return []
    
    json_str = match.group(1)
    
    try:
        cards = json.loads(json_str)
        print(f"✅ 成功加载 {len(cards)} 张虾虾卡")
        return cards
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return []

def get_effect_power(effect_name, attack_value=0):
    """根据效果名称获取效果战斗力"""
    
    effect_power_map = {
        "无": 0,
        "剧毒": 20,  # 5费用对应18-23战斗力，取平均值20
        "抽牌": 11,  # 3费用对应9-13战斗力，取平均值11
        "调度": 8,   # 2费用对应7-9战斗力，取平均值8
        "圣盾": attack_value,  # 圣盾价值等于虾虾攻击力
        "冲锋": 7,   # 1-2费用对应5-9战斗力，取平均值7
        "嘲讽": 4,   # 0.5-1.5费用对应2-7战斗力，取平均值4
    }
    
    # 检查效果名称是否包含关键词
    for key, value in effect_power_map.items():
        if key in effect_name:
            if key == "圣盾":
                return attack_value  # 圣盾价值等于攻击力
            return value
    
    return 0  # 未知效果

def calculate_base_power(attack, health):
    """计算基础战斗力"""
    # 基础战斗力 = 攻击力 + 生命值
    return attack + health

def get_cost_from_total_power(total_power):
    """根据总战斗力查表确定费用"""
    
    # 费用-战斗力关系表（根据balance_strategy_display.html）
    cost_power_ranges = [
        (0, 0, 5),      # 0费: 0-5战斗力
        (1, 5, 7),      # 1费: 5-7战斗力
        (2, 7, 9),      # 2费: 7-9战斗力
        (3, 9, 13),     # 3费: 9-13战斗力
        (4, 13, 18),    # 4费: 13-18战斗力
        (5, 18, 23),    # 5费: 18-23战斗力
        (6, 23, 30),    # 6费: 23-30战斗力
        (7, 30, 38),    # 7费: 30-38战斗力
        (8, 38, 47),    # 8费: 38-47战斗力
        (9, 47, 57),    # 9费: 47-57战斗力
        (10, 55, 82),   # 10费: 55-82战斗力（注意范围有重叠）
    ]
    
    for cost, min_power, max_power in cost_power_ranges:
        if min_power <= total_power <= max_power:
            return cost
    
    # 如果超出范围，使用最接近的费用
    if total_power < 0:
        return 0
    elif total_power > 82:
        return 10  # 最大10费
    
    # 线性插值
    for i in range(len(cost_power_ranges) - 1):
        cost1, min1, max1 = cost_power_ranges[i]
        cost2, min2, max2 = cost_power_ranges[i + 1]
        
        if max1 <= total_power <= min2:
            # 在两个范围之间
            return cost1 if total_power < (max1 + min2) / 2 else cost2
    
    return 5  # 默认5费

def apply_personality_formula(attack, health, personality):
    """应用性格公式调整攻击力和生命值"""
    
    # 性格系数表（根据balance_strategy_display.html）
    personality_coefficients = {
        "勇敢": {"attack_mult": 0.85, "health_mult": 1.05, "base_mult": 1.00},
        "智慧": {"attack_mult": 1.05, "health_mult": 0.85, "base_mult": 1.00},
        "狡猾": {"attack_mult": 0.90, "health_mult": 1.00, "base_mult": 1.00},
        "沉稳": {"attack_mult": 1.00, "health_mult": 0.90, "base_mult": 1.00},
        "狂野": {"attack_mult": 0.70, "health_mult": 1.20, "base_mult": 1.00},  # 攻击极端
    }
    
    if personality not in personality_coefficients:
        print(f"⚠️ 未知性格: {personality}，使用默认系数")
        return attack, health
    
    coeff = personality_coefficients[personality]
    
    # 应用系数反转逻辑：系数低表示该属性更高效
    # 对于攻击型（勇敢），攻击系数低(0.85)意味着攻击力更高
    # 对于防御型（智慧），生命系数低(0.85)意味着生命值更高
    
    # 计算基础数值（假设基础战斗力相同）
    base_power = attack + health
    
    # 根据系数分配攻击力和生命值
    # 系数越低，该属性获得更多分配
    total_coeff = coeff['attack_mult'] + coeff['health_mult']
    
    # 攻击力比例 = 生命系数 / 总系数（因为生命系数高表示攻击力分配少）
    attack_ratio = coeff['health_mult'] / total_coeff
    health_ratio = coeff['attack_mult'] / total_coeff
    
    # 调整攻击力和生命值，保持总战斗力不变
    new_attack = base_power * attack_ratio
    new_health = base_power * health_ratio
    
    return round(new_attack, 1), round(new_health, 1)

def recalculate_card(card):
    """重新计算单张虾虾卡"""
    
    # 提取原始数据
    original_attack = card.get('attack', 0)
    original_health = card.get('health', 0)
    personality = card.get('personality', '')
    effect = card.get('effect', '无')
    original_cost = card.get('cost', 0)
    
    # 1. 应用性格公式调整攻击力和生命值
    adjusted_attack, adjusted_health = apply_personality_formula(
        original_attack, original_health, personality
    )
    
    # 2. 计算基础战斗力
    base_power = calculate_base_power(adjusted_attack, adjusted_health)
    
    # 3. 计算效果战斗力
    effect_power = get_effect_power(effect, adjusted_attack)
    
    # 4. 计算总战斗力
    total_power = base_power + effect_power
    
    # 5. 根据总战斗力确定费用
    new_cost = get_cost_from_total_power(total_power)
    
    # 6. 确保有效果虾虾的费用不低于效果基础费用
    if effect != "无":
        effect_base_cost = {
            "剧毒": 5,
            "抽牌": 3,
            "调度": 2,
            "圣盾": 0,  # 圣盾没有固定基础费用
            "冲锋": 1,
            "嘲讽": 1,
        }
        
        for key, min_cost in effect_base_cost.items():
            if key in effect:
                new_cost = max(new_cost, min_cost)
                break
    
    # 更新卡牌数据
    updated_card = card.copy()
    updated_card['attack'] = adjusted_attack
    updated_card['health'] = adjusted_health
    updated_card['base_power'] = round(base_power, 1)
    updated_card['total_power'] = round(total_power, 1)
    updated_card['cost'] = new_cost
    
    return updated_card

def main():
    print("🎴 Open-Gi-Oh! 虾虾卡重新评估")
    print("=" * 60)
    
    # 加载虾虾卡数据
    cards = load_shrimp_cards()
    
    if not cards:
        print("❌ 无法加载虾虾卡数据，退出")
        return
    
    # 重新评估每张虾虾卡
    print("\n🔧 重新评估虾虾卡...")
    updated_cards = []
    changes_summary = []
    
    for i, card in enumerate(cards, 1):
        original_card = card.copy()
        updated_card = recalculate_card(card)
        updated_cards.append(updated_card)
        
        # 记录变化
        if (original_card['cost'] != updated_card['cost'] or
            original_card['attack'] != updated_card['attack'] or
            original_card['health'] != updated_card['health']):
            
            change = {
                'id': card['id'],
                'name': card['name'],
                'original_cost': original_card['cost'],
                'new_cost': updated_card['cost'],
                'original_attack': original_card['attack'],
                'new_attack': round(updated_card['attack'], 1),
                'original_health': original_card['health'],
                'new_health': round(updated_card['health'], 1),
                'effect': card['effect'],
                'personality': card['personality']
            }
            changes_summary.append(change)
        
        print(f"  [{i:2d}/{len(cards)}] {card['name']:15} 费用: {original_card['cost']}→{updated_card['cost']} 攻击: {original_card['attack']}→{round(updated_card['attack'], 1)} 生命: {original_card['health']}→{round(updated_card['health'], 1)}")
    
    print(f"\n✅ 重新评估完成！{len(changes_summary)} 张卡牌有变化")
    
    # 输出变化摘要
    if changes_summary:
        print("\n📊 **变化摘要**:")
        print(f"{'ID':<15} {'名称':<15} {'费用':<8} {'攻击力':<10} {'生命值':<10} {'效果':<10} {'性格':<8}")
        print("-" * 85)
        
        for change in changes_summary:
            cost_change = f"{change['original_cost']}→{change['new_cost']}"
            attack_change = f"{change['original_attack']}→{change['new_attack']}"
            health_change = f"{change['original_health']}→{change['new_health']}"
            
            print(f"{change['id']:<15} {change['name']:<15} {cost_change:<8} {attack_change:<10} {health_change:<10} {change['effect']:<10} {change['personality']:<8}")
    
    # 生成新的JS文件
    output_js = f"const balancedShrimpCards30HP = {json.dumps(updated_cards, ensure_ascii=False, indent=2)};"
    
    with open('balanced_shrimp_cards_30hp_recalculated.js', 'w', encoding='utf-8') as f:
        f.write(output_js)
    
    print(f"\n💾 新的虾虾卡数据已保存到: balanced_shrimp_cards_30hp_recalculated.js")
    print(f"   卡牌数量: {len(updated_cards)}")
    print(f"   有变化的卡牌: {len(changes_summary)}")
    
    # 生成替换脚本
    create_replacement_script(updated_cards)

def create_replacement_script(updated_cards):
    """创建HTML页面替换脚本"""
    
    print("\n🔧 创建页面替换脚本...")
    
    # 创建更新脚本
    update_script = """#!/usr/bin/env python3
"""
    update_script += """\"\"\"
🎴 Open-Gi-Oh! 虾虾卡页面更新脚本
用重新评估后的数据更新HTML页面
\"\"\"

import re

def update_html_file():
    \"\"\"更新HTML文件中的虾虾卡数据\"\"\"
    
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
"""
    
    with open('update_shrimp_cards_page.py', 'w', encoding='utf-8') as f:
        f.write(update_script)
    
    print("✅ 页面更新脚本已创建: update_shrimp_cards_page.py")
    print("   运行命令: python3 update_shrimp_cards_page.py")

if __name__ == "__main__":
    main()