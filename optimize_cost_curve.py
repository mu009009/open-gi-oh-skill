#!/usr/bin/env python3
"""
🎴 Open-Gi-Oh! 费用-战斗力曲线优化脚本
目标：10费战斗力是0费的12倍，1费的10倍
"""

import math

def calculate_new_cost_curve():
    """
    计算新的费用-战斗力曲线
    目标比例：10费 = 12倍(0费) = 10倍(1费)
    使用指数增长曲线，但早期增长较慢，后期增长更快
    """
    
    # 目标值：10费战斗力应该是0费的12倍
    # 假设0费平均战斗力 = 5（维持原状）
    zero_cost_avg = 5.0
    
    # 10费平均战斗力 = 12 * 0费 = 60
    ten_cost_avg = zero_cost_avg * 12  # = 60
    
    # 1费平均战斗力 = 10费 / 10 = 6
    one_cost_avg = ten_cost_avg / 10   # = 6
    
    print(f"目标平均值：")
    print(f"  0费: {zero_cost_avg}")
    print(f"  1费: {one_cost_avg}")
    print(f"  10费: {ten_cost_avg}")
    print(f"  比例检查：10费/0费 = {ten_cost_avg/zero_cost_avg:.1f}倍")
    print(f"  比例检查：10费/1费 = {ten_cost_avg/one_cost_avg:.1f}倍")
    
    # 使用二次函数曲线：y = a*x^2 + b*x + c
    # 已知三点：(0, 5), (1, 6), (10, 60)
    # 解方程组得到系数
    
    # 解方程组：
    # c = 5  (x=0时)
    # a + b + 5 = 6  => a + b = 1
    # 100a + 10b + 5 = 60  => 100a + 10b = 55
    
    # 从 a+b=1 得 b=1-a
    # 代入：100a + 10(1-a) = 55
    # 100a + 10 - 10a = 55
    # 90a = 45
    # a = 0.5
    # b = 0.5
    
    a = 0.5
    b = 0.5
    c = zero_cost_avg
    
    print(f"\n二次函数系数：a={a}, b={b}, c={c}")
    print(f"公式：战斗力 = {a}*费用² + {b}*费用 + {c}")
    
    # 计算每个费用的战斗力
    cost_power = {}
    for cost in range(0, 11):
        power = a * (cost**2) + b * cost + c
        # 添加一些随机性范围：±20%
        min_power = power * 0.8
        max_power = power * 1.2
        cost_power[cost] = {
            'avg': round(power, 1),
            'min': round(min_power, 1),
            'max': round(max_power, 1),
            'range': f"{int(min_power)}-{int(max_power)}"
        }
    
    return cost_power

def calculate_growth_factors(cost_power):
    """计算增长因子"""
    print(f"\n📈 费用-战斗力增长分析：")
    print(f"{'费用':<4} {'平均战斗力':<10} {'范围':<15} {'环比增长':<12} {'基准比':<12}")
    print("-" * 60)
    
    base_0 = cost_power[0]['avg']
    base_1 = cost_power[1]['avg']
    
    for cost in range(0, 11):
        power = cost_power[cost]
        avg = power['avg']
        
        # 环比增长（相对前一费用）
        if cost > 0:
            prev_avg = cost_power[cost-1]['avg']
            growth = avg / prev_avg
            growth_str = f"{growth:.2f}x"
        else:
            growth_str = "-"
        
        # 相对于0费的比例
        ratio_to_0 = avg / base_0
        ratio_to_0_str = f"{ratio_to_0:.2f}x"
        
        print(f"{cost:<4} {avg:<10.1f} {power['range']:<15} {growth_str:<12} {ratio_to_0_str:<12}")

def update_html_table(cost_power):
    """生成新的HTML表格代码"""
    print(f"\n📋 新的费用-战斗力表格：")
    
    # 定义类别
    categories = {
        0: "工具牌",
        1: "前期牌",
        2: "前期牌",
        3: "前期牌",
        4: "中期牌",
        5: "中期牌",
        6: "中期牌",
        7: "后期牌",
        8: "后期牌",
        9: "后期牌",
        10: "终结牌"
    }
    
    # 定义交换限制
    exchange_rules = {
        0: "只能交换0-1费卡",
        1: "最多交换2费卡",
        2: "最多交换3费卡",
        3: "最多交换4费卡",
        4: "最多交换5费卡",
        5: "最多交换6费卡",
        6: "最多交换7费卡",
        7: "最多交换8费卡",
        8: "最多交换9费卡",
        9: "最多交换10费卡",
        10: "应有终结游戏能力"
    }
    
    print(f"{'费用':<4} {'战斗力范围':<15} {'类别':<10} {'交换限制':<25}")
    print("-" * 60)
    
    html_rows = []
    for cost in range(0, 11):
        power = cost_power[cost]
        category = categories[cost]
        exchange = exchange_rules[cost]
        
        print(f"{cost:<4} {power['range']:<15} {category:<10} {exchange:<25}")
        
        # 生成HTML行
        html_row = f"""                            <tr>
                                <td><strong>{cost}费</strong></td>
                                <td>{power['range']}</td>
                                <td>{category}</td>
                                <td>{exchange}</td>
                            </tr>"""
        html_rows.append(html_row)
    
    return "\n".join(html_rows)

def calculate_wish_personality_aesthetics_formulas():
    """计算愿望、性格、审美对应的战斗力计算公式"""
    print(f"\n🎭 愿望、性格、审美战斗力计算公式分析")
    print("=" * 60)
    
    # 从shrimp_formulas.json分析现有的公式
    print("当前公式结构：")
    print("战斗力 = base_multiplier * (attack_mult * attack + health_mult * health)")
    print("其中：")
    print("  - base_multiplier: 基础比例系数 (愿望+性格+审美组合决定)")
    print("  - attack_mult: 攻击力乘数 (性格偏攻击型时较高)")
    print("  - health_mult: 生命值乘数 (性格偏防御型时较高)")
    print("  - variability: 随机性因子 (±10%)")
    
    print(f"\n示例组合分析：")
    combinations = [
        ("神秘", "勇敢", "梦幻"),
        ("神秘", "智慧", "酷炫"),
        ("热情", "勇敢", "华丽"),
        ("热情", "智慧", "清新")
    ]
    
    for wish, personality, aesthetic in combinations:
        # 模拟计算
        base = 1.0 + (hash(wish) % 100)/1000  # 简单模拟
        if personality == "勇敢":
            attack_mult = 1.1
            health_mult = 0.9
        else:  # 智慧
            attack_mult = 0.9
            health_mult = 1.1
        
        if aesthetic == "梦幻":
            aesthetic_bonus = 1.05
        elif aesthetic == "酷炫":
            aesthetic_bonus = 1.1
        elif aesthetic == "华丽":
            aesthetic_bonus = 1.08
        elif aesthetic == "清新":
            aesthetic_bonus = 0.95
        else:
            aesthetic_bonus = 1.0
        
        total_mult = base * attack_mult * health_mult * aesthetic_bonus
        
        print(f"  {wish}_{personality}_{aesthetic}:")
        print(f"    基础系数: {base:.3f}, 攻击乘数: {attack_mult:.2f}, 生命乘数: {health_mult:.2f}")
        print(f"    审美加成: {aesthetic_bonus:.2f}, 总系数: {total_mult:.3f}")
        print(f"    示例：攻击10/生命10 → 战斗力: {total_mult * (10*attack_mult + 10*health_mult):.1f}")

def main():
    print("🎴 Open-Gi-Oh! 平衡策略优化")
    print("=" * 60)
    
    # 1. 重新计算费用-战斗力曲线
    cost_power = calculate_new_cost_curve()
    
    # 2. 分析增长因子
    calculate_growth_factors(cost_power)
    
    # 3. 生成新的HTML表格
    html_table = update_html_table(cost_power)
    
    # 4. 分析愿望、性格、审美计算公式
    calculate_wish_personality_aesthetics_formulas()
    
    print(f"\n🔥 优化完成！")
    print(f"主要改进：")
    print(f"  1. 10费战斗力调整为0费的12倍（原121倍）")
    print(f"  2. 10费战斗力调整为1费的10倍（原30倍）")
    print(f"  3. 费用-战斗力曲线更平滑")
    print(f"  4. 高费卡不再过度强势，游戏曲线更合理")
    
    # 保存HTML表格到文件
    with open("new_cost_table.html", "w", encoding="utf-8") as f:
        f.write(html_table)
    print(f"\n✅ 新的表格已保存到：new_cost_table.html")

if __name__ == "__main__":
    main()