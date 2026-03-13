#!/usr/bin/env python3
"""
🎴 Open-Gi-Oh! 虾虾卡重新评估脚本（修正版）
根据新的平衡策略重新计算50张虾虾卡的数值和费用
修正基础战斗力计算错误
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
        "冻结": 5,   # 估计值
        "连击": 8,   # 估计值
        "超杀": 10,  # 估计值
        "复生": 12,  # 估计值
        "免疫": 15,  # 估计值
        "光环": 6,   # 估计值
        "亡语": 7,   # 估计值
        "风怒": 9,   # 估计值
    }
    
    # 检查效果名称是否包含关键词
    for key, value in effect_power_map.items():
        if key in effect_name:
            if key == "圣盾":
                return min(attack_value, 15)  # 圣盾价值不超过15
            return value
    
    return 0  # 未知效果

def scale_attack_health(original_attack, original_health):
    """缩放攻击力和生命值到合理范围"""
    # 原始数据中攻击力和生命值都太大（18-30），需要缩小
    # 根据费用表：5费用对应总战斗力20左右
    # 所以攻击力应该在5-15范围内，生命值在5-15范围内
    
    # 计算缩放比例
    original_total = original_attack + original_health
    
    # 目标总数值：20-40（对应合理的攻击力+生命值）
    if original_total > 50:
        scale_factor = 0.4  # 大幅缩小
    elif original_total > 40:
        scale_factor = 0.5
    elif original_total > 30:
        scale_factor = 0.6
    else:
        scale_factor = 0.7
    
    scaled_attack = max(3, round(original_attack * scale_factor))
    scaled_health = max(3, round(original_health * scale_factor))
    
    return scaled_attack, scaled_health

def apply_personality_adjustment(attack, health, personality):
    """根据性格调整攻击力和生命值"""
    
    # 性格调整系数（基于系数反转理解）
    # 勇敢：攻击型，攻击力更高
    # 智慧：防御型，生命值更高
    # 狡猾：攻击略高
    # 沉稳：生命略高
    # 狂野：极端（攻击或生命）
    
    personality_adjustments = {
        "勇敢": {"attack_mult": 1.2, "health_mult": 0.9},   # 攻击+20%，生命-10%
        "智慧": {"attack_mult": 0.9, "health_mult": 1.2},   # 攻击-10%，生命+20%
        "狡猾": {"attack_mult": 1.1, "health_mult": 0.95},  # 攻击+10%，生命-5%
        "沉稳": {"attack_mult": 0.95, "health_mult": 1.1},  # 攻击-5%，生命+10%
        "狂野": {"attack_mult": 1.3, "health_mult": 0.8},   # 攻击+30%，生命-20%（攻击极端）
    }
    
    if personality not in personality_adjustments:
        return attack, health
    
    adjustment = personality_adjustments[personality]
    
    new_attack = max(1, round(attack * adjustment['attack_mult']))
    new_health = max(1, round(health * adjustment['health_mult']))
    
    return new_attack, new_health

def calculate_base_power(attack, health):
    """计算基础战斗力（修正版）"""
    # 基础战斗力 = 攻击力 + 生命值
    # 但需要适当加权，因为攻击力通常比生命值更有价值
    return attack * 1.2 + health * 0.8

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
        (10, 55, 82),   # 10费: 55-82战斗力
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
    
    return round(total_power / 8)  # 简单估算

def recalculate_card(card):
    """重新计算单张虾虾卡（修正版）"""
    
    # 提取原始数据
    original_attack = card.get('attack', 0)
    original_health = card.get('health', 0)
    personality = card.get('personality', '')
    effect = card.get('effect', '无')
    original_cost = card.get('cost', 0)
    
    # 1. 缩放攻击力和生命值到合理范围
    scaled_attack, scaled_health = scale_attack_health(original_attack, original_health)
    
    # 2. 应用性格调整
    adjusted_attack, adjusted_health = apply_personality_adjustment(scaled_attack, scaled_health, personality)
    
    # 3. 计算基础战斗力
    base_power = calculate_base_power(adjusted_attack, adjusted_health)
    
    # 4. 计算效果战斗力
    effect_power = get_effect_power(effect, adjusted_attack)
    
    # 5. 计算总战斗力
    total_power = base_power + effect_power
    
    # 6. 根据总战斗力确定费用
    new_cost = get_cost_from_total_power(total_power)
    
    # 7. 确保有效果虾虾的费用不低于效果基础费用
    if effect != "无":
        effect_base_cost = {
            "剧毒": 5,
            "抽牌": 3,
            "调度": 2,
            "圣盾": 0,  # 圣盾没有固定基础费用
            "冲锋": 1,
            "嘲讽": 1,
            "冻结": 2,
            "连击": 2,
            "超杀": 3,
            "复生": 4,
            "免疫": 4,
            "光环": 2,
            "亡语": 2,
            "风怒": 3,
        }
        
        for key, min_cost in effect_base_cost.items():
            if key in effect:
                new_cost = max(new_cost, min_cost)
                break
    
    # 8. 限制费用范围
    new_cost = max(0, min(10, new_cost))
    
    # 更新卡牌数据
    updated_card = card.copy()
    updated_card['attack'] = adjusted_attack
    updated_card['health'] = adjusted_health
    updated_card['base_power'] = round(base_power, 1)
    updated_card['total_power'] = round(total_power, 1)
    updated_card['cost'] = new_cost
    
    return updated_card

def main():
    print("🎴 Open-Gi-Oh! 虾虾卡重新评估（修正版）")
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
                'new_attack': updated_card['attack'],
                'original_health': original_card['health'],
                'new_health': updated_card['health'],
                'effect': card['effect'],
                'personality': card['personality']
            }
            changes_summary.append(change)
        
        print(f"  [{i:2d}/{len(cards)}] {card['name']:15} 费用: {original_card['cost']}→{updated_card['cost']} 攻击: {original_card['attack']}→{updated_card['attack']} 生命: {original_card['health']}→{updated_card['health']}")
    
    print(f"\n✅ 重新评估完成！{len(changes_summary)} 张卡牌有变化")
    
    # 输出变化摘要
    if changes_summary:
        print("\n📊 **变化摘要** (前20张):")
        print(f"{'ID':<15} {'名称':<15} {'费用':<8} {'攻击力':<10} {'生命值':<10} {'效果':<10} {'性格':<8}")
        print("-" * 85)
        
        for change in changes_summary[:20]:
            cost_change = f"{change['original_cost']}→{change['new_cost']}"
            attack_change = f"{change['original_attack']}→{change['new_attack']}"
            health_change = f"{change['original_health']}→{change['new_health']}"
            
            print(f"{change['id']:<15} {change['name']:<15} {cost_change:<8} {attack_change:<10} {health_change:<10} {change['effect']:<10} {change['personality']:<8}")
        
        if len(changes_summary) > 20:
            print(f"... 还有 {len(changes_summary)-20} 张卡牌变化")
    
    # 生成新的JS文件
    output_js = f"const balancedShrimpCards30HP = {json.dumps(updated_cards, ensure_ascii=False, indent=2)};"
    
    with open('balanced_shrimp_cards_30hp_recalculated_corrected.js', 'w', encoding='utf-8') as f:
        f.write(output_js)
    
    print(f"\n💾 新的虾虾卡数据已保存到: balanced_shrimp_cards_30hp_recalculated_corrected.js")
    print(f"   卡牌数量: {len(updated_cards)}")
    print(f"   有变化的卡牌: {len(changes_summary)}")
    
    # 统计费用分布
    print("\n📊 **费用分布统计**:")
    cost_distribution = {}
    for card in updated_cards:
        cost = card['cost']
        cost_distribution[cost] = cost_distribution.get(cost, 0) + 1
    
    for cost in sorted(cost_distribution.keys()):
        count = cost_distribution[cost]
        print(f"  {cost}费: {count}张 ({count/len(updated_cards)*100:.1f}%)")
    
    # 生成页面更新命令
    print(f"\n🔧 **更新页面命令**:")
    print(f"  cp balanced_shrimp_cards_30hp_recalculated_corrected.js balanced_shrimp_cards_30hp.js")
    print(f"  然后访问: http://118.196.117.234:8080/open-gi-oh-web/final_shrimp_cards_preview.html")

if __name__ == "__main__":
    main()