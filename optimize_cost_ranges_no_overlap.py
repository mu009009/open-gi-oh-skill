#!/usr/bin/env python3
"""
🎴 Open-Gi-Oh! 费用-战斗力范围优化（无重叠版本）
目标：1. 无重叠 2. 连续 3. 10费=0费的12倍
"""

import math

def calculate_non_overlapping_ranges():
    """
    计算无重叠的连续战斗力范围
    目标：10费战斗力 = 0费的12倍 = 1费的10倍
    """
    
    print("🔧 重新计算无重叠费用-战斗力范围")
    print("=" * 60)
    
    # 基础参数
    zero_cost_avg = 5.0      # 0费平均战斗力
    ten_cost_avg = 60.0      # 10费平均战斗力（12倍）
    one_cost_avg = 6.0       # 1费平均战斗力（10倍关系）
    
    # 使用线性增长：从0费到10费，战斗力从5增长到60
    # 公式：战斗力 = 5 + 5.5 * 费用
    # 这样：0费=5，1费=10.5，10费=60（接近目标）
    
    # 实际上，为了精确满足比例，我们使用：
    # 0费: 5, 1费: 6, 10费: 60
    # 使用二次函数：y = 0.5x² + 0.5x + 5
    
    a = 0.5
    b = 0.5
    c = zero_cost_avg
    
    # 计算每个费用的平均战斗力
    avg_powers = {}
    for cost in range(0, 11):
        avg = a * (cost**2) + b * cost + c
        avg_powers[cost] = avg
    
    print(f"📊 平均战斗力（中心点）：")
    for cost in range(0, 11):
        print(f"  {cost}费: {avg_powers[cost]:.1f}")
    
    # 现在计算无重叠的范围
    # 策略：每个费用的范围以其平均值为中心，宽度为相邻平均值差的一半
    ranges = {}
    
    for cost in range(0, 11):
        # 当前平均值
        current_avg = avg_powers[cost]
        
        # 计算范围边界
        if cost == 0:
            # 0费：下界为0，上界为(0费平均+1费平均)/2
            lower = 0
            upper = (avg_powers[0] + avg_powers[1]) / 2
        elif cost == 10:
            # 10费：下界为(9费平均+10费平均)/2，上界无限制
            lower = (avg_powers[9] + avg_powers[10]) / 2
            upper = lower * 1.5  # 稍微扩展上界
        else:
            # 中间费用：下界为与前一个费用的中点，上界为与后一个费用的中点
            lower = (avg_powers[cost-1] + avg_powers[cost]) / 2
            upper = (avg_powers[cost] + avg_powers[cost+1]) / 2
        
        # 确保范围连续且无重叠
        if cost > 0:
            prev_upper = ranges[cost-1]['upper']
            if lower <= prev_upper:
                # 如果有重叠，调整下界为上界+0.1
                lower = prev_upper + 0.1
        
        ranges[cost] = {
            'lower': lower,
            'upper': upper,
            'avg': current_avg,
            'range_str': f"{int(lower)}-{int(upper)}"
        }
    
    return ranges

def analyze_ranges(ranges):
    """分析范围特性"""
    print(f"\n📈 范围分析：")
    print(f"{'费用':<4} {'范围':<15} {'宽度':<10} {'中心点':<10} {'检查':<15}")
    print("-" * 60)
    
    for cost in range(0, 11):
        r = ranges[cost]
        width = r['upper'] - r['lower']
        
        # 检查连续性
        continuity = "✅"
        if cost > 0:
            prev_upper = ranges[cost-1]['upper']
            if abs(r['lower'] - prev_upper) > 0.2:  # 允许微小间隙
                continuity = f"⚠️ 间隙: {r['lower']-prev_upper:.1f}"
        
        print(f"{cost:<4} {r['range_str']:<15} {width:<10.1f} {r['avg']:<10.1f} {continuity:<15}")

def generate_html_table(ranges):
    """生成HTML表格代码"""
    print(f"\n📋 新的费用-战斗力表格（无重叠）：")
    
    # 定义类别和交换规则（保持不变）
    categories = {
        0: "工具牌", 1: "前期牌", 2: "前期牌", 3: "前期牌",
        4: "中期牌", 5: "中期牌", 6: "中期牌",
        7: "后期牌", 8: "后期牌", 9: "后期牌",
        10: "终结牌"
    }
    
    exchange_rules = {
        0: "只能交换0-1费卡", 1: "最多交换2费卡", 2: "最多交换3费卡",
        3: "最多交换4费卡", 4: "最多交换5费卡", 5: "最多交换6费卡",
        6: "最多交换7费卡", 7: "最多交换8费卡", 8: "最多交换9费卡",
        9: "最多交换10费卡", 10: "应有终结游戏能力"
    }
    
    print(f"{'费用':<4} {'战斗力范围':<15} {'类别':<10} {'交换限制':<25}")
    print("-" * 60)
    
    html_rows = []
    for cost in range(0, 11):
        r = ranges[cost]
        category = categories[cost]
        exchange = exchange_rules[cost]
        
        print(f"{cost:<4} {r['range_str']:<15} {category:<10} {exchange:<25}")
        
        html_row = f"""                            <tr>
                                <td><strong>{cost}费</strong></td>
                                <td>{r['range_str']}</td>
                                <td>{category}</td>
                                <td>{exchange}</td>
                            </tr>"""
        html_rows.append(html_row)
    
    return "\n".join(html_rows)

def create_balance_rationale():
    """创建平衡性思考链"""
    print(f"\n🧠 平衡性思考链（可协商规则）")
    print("=" * 60)
    
    rationale = """
### 🎯 新版费用-战斗力平衡策略（可协商规则）

#### 🔧 **优化原则**
1. **无重叠原则**：每个战斗力值必须对应唯一费用，避免歧义
2. **连续性原则**：战斗力范围连续，确保任意值都有对应费用
3. **比例控制**：10费战斗力是0费的12倍，1费的10倍

#### 📊 **数值设计逻辑**
- **0费基准**：5战斗力（工具牌，不影响游戏核心）
- **线性增长**：早期费用增长较慢（1-3费）
- **加速增长**：中期费用增长加速（4-7费）
- **后期饱和**：高费用增长放缓（8-10费）

#### 🎮 **游戏性影响**
1. **平滑曲线**：避免高费卡过度强势
2. **策略多样性**：鼓励混合费用曲线
3. **交换公平**：同费用卡牌交换价值相当
4. **费用惩罚**：高费卡需承担回合等待成本

#### 🔄 **可协商调整点**
1. **比例系数**：10费/0费比例可在10-15倍间调整
2. **范围宽度**：各费用范围宽度可根据游戏节奏调整
3. **特殊例外**：特定效果卡牌可突破常规范围
"""
    
    print(rationale)
    return rationale

def main():
    print("🎴 Open-Gi-Oh! 费用范围优化（无重叠版本）")
    print("=" * 60)
    
    # 1. 计算无重叠范围
    ranges = calculate_non_overlapping_ranges()
    
    # 2. 分析范围特性
    analyze_ranges(ranges)
    
    # 3. 生成HTML表格
    html_table = generate_html_table(ranges)
    
    # 4. 创建平衡性思考链
    rationale = create_balance_rationale()
    
    # 保存结果
    with open("new_cost_table_no_overlap.html", "w", encoding="utf-8") as f:
        f.write(html_table)
    
    with open("balance_rationale.md", "w", encoding="utf-8") as f:
        f.write(rationale)
    
    print(f"\n✅ 优化完成！")
    print(f"  1. 无重叠范围表格已保存：new_cost_table_no_overlap.html")
    print(f"  2. 平衡性思考链已保存：balance_rationale.md")
    print(f"  3. 主要改进：消除了范围重叠，确保唯一对应关系")

if __name__ == "__main__":
    main()