#!/usr/bin/env python3
# Open-Gi-Oh! 虾虾卡牌生成器 (30血量版)
# 基于新的平衡策略重新计算所有数值
# 创建时间: 2026-03-12

import json
import random
import math
from datetime import datetime

class ShrimpGenerator30HP:
    """基于30血量平衡策略的虾虾卡牌生成器"""
    
    def __init__(self):
        # 基础属性
        self.wishes = ["霸气", "魅力", "智慧", "自由", "战斗"]
        self.personalities = ["勇敢", "智慧", "狡猾", "沉稳", "狂野"]
        self.aesthetics = ["华丽", "简约", "奇幻", "科技", "自然"]
        self.rarities = ["普通", "稀有", "超级稀有", "传说"]
        
        # 30血量版的战斗力-费用转换表
        self.cost_table = {
            0: (0, 5),       # 0费: 战斗力0-5
            1: (5, 15),      # 1费: 战斗力5-15
            2: (15, 30),     # 2费: 战斗力15-30
            3: (30, 50),     # 3费: 战斗力30-50
            4: (50, 75),     # 4费: 战斗力50-75
            5: (75, 105),    # 5费: 战斗力75-105
            6: (105, 140),   # 6费: 战斗力105-140
            7: (140, 180),   # 7费: 战斗力140-180
            8: (180, 225),   # 8费: 战斗力180-225
            9: (225, 275),   # 9费: 战斗力225-275
            10: (275, 330)   # 10费: 战斗力275-330
        }
        
        # 特殊效果战斗力价值 (30血量版)
        self.effect_values = {
            "剧毒": 60,      # 5费用价值 (60战斗力)
            "抽牌": 40,      # 3费用价值 (40战斗力)
            "调度": 25,      # 2费用价值 (25战斗力)
            "圣盾": None,    # 变值: =虾虾攻击力
            "冲锋": 15,      # 1-2费用价值
            "嘲讽": 10,      # 0.5-1.5费用价值
            "连击": 20,      # 额外攻击一次
            "亡语": 30,      # 死亡时触发效果
            "风怒": 25,      # 每回合攻击两次
            "免疫": 35,      # 免疫伤害和效果
            "冻结": 20,      # 使目标无法攻击
            "光环": 30,      # 为友方提供增益
            "超杀": 25,      # 溢出伤害转化
            "复生": 35       # 死亡后复活
        }
        
        # 性格对攻击/生命的偏好系数 (30血量版调整)
        self.personality_biases = {
            "勇敢": {"attack_bias": 0.7, "health_bias": 0.3},    # 攻击型
            "智慧": {"attack_bias": 0.4, "health_bias": 0.6},    # 生存型
            "狡猾": {"attack_bias": 0.6, "health_bias": 0.4},    # 平衡偏攻击
            "沉稳": {"attack_bias": 0.3, "health_bias": 0.7},    # 防御型
            "狂野": {"attack_bias": 0.8, "health_bias": 0.2}     # 极端攻击
        }
        
        # 愿望对基础战斗力的影响 (30血量版)
        self.wish_multipliers = {
            "霸气": 1.2,   # 攻击倾向
            "魅力": 0.9,   # 效果倾向
            "智慧": 1.1,   # 平衡偏智
            "自由": 1.0,   # 平衡
            "战斗": 1.3    # 战斗倾向
        }
        
        # 审美对稀有度的影响
        self.aesthetic_rarity_weights = {
            "华丽": {"传说": 0.3, "超级稀有": 0.4, "稀有": 0.2, "普通": 0.1},
            "简约": {"传说": 0.1, "超级稀有": 0.2, "稀有": 0.3, "普通": 0.4},
            "奇幻": {"传说": 0.2, "超级稀有": 0.3, "稀有": 0.3, "普通": 0.2},
            "科技": {"传说": 0.25, "超级稀有": 0.35, "稀有": 0.25, "普通": 0.15},
            "自然": {"传说": 0.15, "超级稀有": 0.25, "稀有": 0.35, "普通": 0.25}
        }
    
    def calculate_base_power(self, wish, personality, aesthetic):
        """计算基础战斗力 (30血量版)"""
        # 基础公式: (愿望系数 × 性格系数 × 审美系数) × 基础值
        wish_val = self.wish_multipliers[wish]
        
        # 性格系数: 攻击偏好 + 生命偏好 = 1.0
        personality_bias = self.personality_biases[personality]
        
        # 审美对稀有度的影响，间接影响战斗力
        aesthetic_rarity = self.aesthetic_rarity_weights[aesthetic]
        rarity_factor = sum(
            weight * (i+1)  # 稀有度越高，因子越大
            for i, (rarity, weight) in enumerate(aesthetic_rarity.items())
        ) / 2.5  # 归一化到1.0左右
        
        # 基础战斗力范围: 10-100 (30血量版缩小范围)
        base_power = 20 + random.randint(0, 80)  # 20-100
        
        # 应用所有系数
        total_power = base_power * wish_val * rarity_factor
        
        return int(total_power)
    
    def distribute_attack_health(self, total_power, personality):
        """分配攻击力和生命值 (基于性格偏好)"""
        bias = self.personality_biases[personality]
        
        # 攻击力分配 (基于偏好)
        attack_ratio = bias["attack_bias"]
        health_ratio = bias["health_bias"]
        
        # 确保攻击力≥1，生命值≥1
        attack = max(1, int(total_power * attack_ratio))
        health = max(1, int(total_power * health_ratio))
        
        # 调整总和接近总战斗力
        current_total = attack + health
        if current_total < total_power:
            # 按偏好比例增加
            attack += int((total_power - current_total) * attack_ratio)
            health += int((total_power - current_total) * health_ratio)
        elif current_total > total_power:
            # 按偏好比例减少（但保证最小值）
            reduction = current_total - total_power
            attack_reduce = min(attack - 1, int(reduction * attack_ratio))
            health_reduce = min(health - 1, int(reduction * health_ratio))
            attack -= attack_reduce
            health -= health_reduce
        
        return attack, health
    
    def calculate_total_power(self, attack, health, effect=None):
        """计算总战斗力 (包含效果)"""
        # 基础战斗力公式: 攻击力×1.0 + 生命值×0.5 (30血量版调整)
        base_power = attack * 1.0 + health * 0.5
        
        # 效果战斗力
        effect_power = 0
        if effect and effect in self.effect_values:
            effect_value = self.effect_values[effect]
            if effect_value is None:  # 圣盾类，等于攻击力
                effect_power = attack
            else:
                effect_power = effect_value
        
        total_power = base_power + effect_power
        return int(total_power)
    
    def power_to_cost(self, total_power):
        """根据战斗力确定费用"""
        for cost, (min_power, max_power) in sorted(self.cost_table.items()):
            if min_power <= total_power <= max_power:
                return cost
        
        # 如果超出范围，使用边界值
        if total_power < 0:
            return 0
        elif total_power > 330:
            return 10
        else:
            # 线性插值
            return min(10, max(0, total_power // 33))
    
    def select_effect(self, personality):
        """根据性格选择效果"""
        effect_pools = {
            "勇敢": ["冲锋", "连击", "风怒", "超杀"],
            "智慧": ["圣盾", "免疫", "光环", "抽牌"],
            "狡猾": ["剧毒", "潜行", "冻结", "调度"],
            "沉稳": ["嘲讽", "亡语", "复生", "免疫"],
            "狂野": ["剧毒", "连击", "风怒", "超杀"]
        }
        
        pool = effect_pools.get(personality, [])
        if pool and random.random() < 0.7:  # 70%概率有特殊效果
            return random.choice(pool)
        return None
    
    def determine_rarity(self, aesthetic, cost, has_effect):
        """根据审美、费用和效果确定稀有度"""
        # 基础稀有度权重
        weights = self.aesthetic_rarity_weights[aesthetic].copy()
        
        # 费用越高，稀有度越高
        cost_factor = cost / 10.0
        for rarity in weights:
            if rarity == "传说":
                weights[rarity] *= (1 + cost_factor * 0.5)
            elif rarity == "超级稀有":
                weights[rarity] *= (1 + cost_factor * 0.3)
        
        # 有特殊效果增加稀有度概率
        if has_effect:
            weights["传说"] *= 1.2
            weights["超级稀有"] *= 1.1
        
        # 归一化并选择
        total = sum(weights.values())
        rand = random.random() * total
        
        cumulative = 0
        for rarity, weight in weights.items():
            cumulative += weight
            if rand <= cumulative:
                return rarity
        
        return "普通"
    
    def generate_card(self, card_id):
        """生成一张虾虾卡牌"""
        # 随机选择属性
        wish = random.choice(self.wishes)
        personality = random.choice(self.personalities)
        aesthetic = random.choice(self.aesthetics)
        
        # 计算基础战斗力
        base_power = self.calculate_base_power(wish, personality, aesthetic)
        
        # 分配攻击力和生命值
        attack, health = self.distribute_attack_health(base_power, personality)
        
        # 选择效果
        effect = self.select_effect(personality)
        
        # 计算总战斗力
        total_power = self.calculate_total_power(attack, health, effect)
        
        # 确定费用
        cost = self.power_to_cost(total_power)
        
        # 确定稀有度
        rarity = self.determine_rarity(aesthetic, cost, effect is not None)
        
        # 生成卡牌ID
        if not card_id:
            card_id = f"SHRIMP_{random.randint(100000, 999999)}_{random.randint(1000, 9999)}"
        
        # 构建卡牌对象
        card = {
            "id": card_id,
            "name": f"{wish}{personality}{aesthetic}虾",
            "cost": cost,
            "attack": attack,
            "health": health,
            "wish": wish,
            "personality": personality,
            "aesthetic": aesthetic,
            "rarity": rarity,
            "effect": effect if effect else "无",
            "total_power": total_power,
            "base_power": base_power
        }
        
        return card
    
    def generate_balanced_deck(self, count=50):
        """生成平衡的卡组"""
        deck = []
        
        # 确保每种性格都有代表性
        personality_counts = {p: 0 for p in self.personalities}
        target_per_personality = count // len(self.personalities)
        
        for i in range(count):
            # 优先补充数量不足的性格
            available_personalities = [
                p for p in self.personalities 
                if personality_counts[p] < target_per_personality
            ]
            
            if not available_personalities:
                available_personalities = self.personalities
            
            personality = random.choice(available_personalities)
            personality_counts[personality] += 1
            
            card_id = f"SHRIMP_{i+1:03d}_{random.randint(1000, 9999)}"
            card = self.generate_card(card_id)
            
            # 确保攻击力和生命值在合理范围 (1-30)
            card["attack"] = min(30, max(1, card["attack"]))
            card["health"] = min(30, max(1, card["health"]))
            
            deck.append(card)
        
        return deck
    
    def save_deck(self, deck, filename):
        """保存卡组到文件"""
        data = {
            "version": "1.0.0",
            "player_hp": 30,
            "balance_strategy": "30hp_v1",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "card_count": len(deck),
            "cards": deck
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已保存 {len(deck)} 张卡牌到 {filename}")
        return filename

def main():
    """主函数：生成基于30血量的平衡卡组"""
    print("🎴 Open-Gi-Oh! 虾虾卡牌生成器 (30血量版)")
    print("基于新的平衡策略重新计算所有数值")
    print("玩家血量: 30")
    print("")
    
    # 创建生成器
    generator = ShrimpGenerator30HP()
    
    # 生成50张平衡卡牌
    print("🔄 正在生成50张平衡虾虾卡牌...")
    deck = generator.generate_balanced_deck(50)
    
    # 统计信息
    print("📊 生成完成！统计信息:")
    print(f"卡牌总数: {len(deck)}")
    
    # 费用分布
    cost_dist = {}
    for card in deck:
        cost = card["cost"]
        cost_dist[cost] = cost_dist.get(cost, 0) + 1
    
    print("💰 费用分布:")
    for cost in sorted(cost_dist.keys()):
        print(f"  {cost}费: {cost_dist[cost]}张")
    
    # 性格分布
    personality_dist = {}
    for card in deck:
        personality = card["personality"]
        personality_dist[personality] = personality_dist.get(personality, 0) + 1
    
    print("🎭 性格分布:")
    for personality in sorted(personality_dist.keys()):
        print(f"  {personality}: {personality_dist[personality]}张")
    
    # 保存文件
    output_file = "/root/.openclaw/workspace/open-gi-oh-web/balanced_shrimp_cards_30hp.js"
    generator.save_deck(deck, output_file)
    
    # 创建JS格式文件
    js_content = f"const balancedShrimpCards30HP = {json.dumps(deck, ensure_ascii=False, indent=2)};"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ JS文件已保存: {output_file}")
    print(f"📏 文件大小: {len(js_content)} 字节")
    
    # 显示示例卡牌
    print("")
    print("🦐 示例卡牌 (前5张):")
    for i, card in enumerate(deck[:5]):
        print(f"{i+1}. {card['name']} - {card['cost']}费")
        print(f"   攻击:{card['attack']} 生命:{card['health']} 性格:{card['personality']}")
        print(f"   稀有度:{card['rarity']} 效果:{card['effect']}")
        print(f"   总战斗力:{card['total_power']}")
    
    print("")
    print("🚀 生成完成！基于30血量的平衡卡组已就绪！")

if __name__ == "__main__":
    main()
