// 直接测试数据加载
const fs = require('fs');

console.log("🔍 测试虾虾卡数据加载...");

try {
    const content = fs.readFileSync('balanced_shrimp_cards_30hp.js', 'utf-8');
    
    // 提取JSON数组
    const match = content.match(/const\s+balancedShrimpCards30HP\s*=\s*(\[.*?\]);/s);
    
    if (match) {
        const data = JSON.parse(match[1]);
        console.log(`✅ 成功加载 ${data.length} 张卡牌`);
        
        // 查找魅力狡猾科技虾
        const targetCards = data.filter(card => card.name.includes("魅力狡猾科技虾"));
        console.log(`\n🔍 找到 ${targetCards.length} 张"魅力狡猾科技虾":`);
        
        targetCards.forEach(card => {
            console.log(`  ${card.name} (ID: ${card.id})`);
            console.log(`    费用: ${card.cost} (应该是6或8，不是3!)`);
            console.log(`    攻击力: ${card.attack}`);
            console.log(`    生命值: ${card.health}`);
            console.log(`    效果: ${card.effect}`);
            console.log(`    总战斗力: ${card.total_power || 'N/A'}`);
            console.log("");
        });
        
        // 检查是否有费用为3的卡牌
        const cost3Cards = data.filter(card => card.cost === 3);
        if (cost3Cards.length > 0) {
            console.log(`⚠️ 发现 ${cost3Cards.length} 张费用为3的卡牌:`);
            cost3Cards.forEach(card => {
                console.log(`  ${card.name} (ID: ${card.id}) - 攻击力: ${card.attack}, 生命值: ${card.health}`);
            });
        } else {
            console.log("✅ 没有费用为3的卡牌，数据正确！");
        }
    } else {
        console.log("❌ 无法提取数据");
    }
} catch (error) {
    console.log(`❌ 加载失败: ${error.message}`);
}
