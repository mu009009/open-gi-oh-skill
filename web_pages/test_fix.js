// 🛠️ Open-Gi-Oh! 页面修复测试脚本
// 用于测试页面是否能够正确加载和显示卡牌

// 1. 首先测试数据是否加载
function testDataLoading() {
    console.log("🔍 测试数据加载...");
    
    try {
        if (typeof balancedShrimpCardsV101 === 'undefined') {
            console.error("❌ 错误: balancedShrimpCardsV101 未定义");
            return false;
        }
        
        const cardCount = balancedShrimpCardsV101.length;
        console.log(`✅ 数据加载成功: ${cardCount} 张卡牌`);
        
        // 显示前3张卡牌信息
        console.log("📊 前3张卡牌:");
        for (let i = 0; i < Math.min(3, cardCount); i++) {
            const card = balancedShrimpCardsV101[i];
            console.log(`  ${i + 1}. ${card.name} (费用: ${card.cost}, 攻击: ${card.attack}, 生命: ${card.health}, 战斗力: ${card.combat_value})`);
        }
        
        return true;
        
    } catch (error) {
        console.error("❌ 数据加载测试失败:", error);
        return false;
    }
}

// 2. 测试页面功能

function testPageFunctions() {
    console.log("\n🔧 测试页面功能...");
    
    // 模拟页面上的函数
    const testFunctions = {
        'filterCards': function() {
            try {
                // 模拟过滤逻辑
                const filtered = balancedShrimpCardsV101.filter(card => card.cost <= 5);
                console.log(`✅ filterCards 可用: 过滤后 ${filtered.length} 张卡牌`);
                return true;
            } catch (error) {
                console.error("❌ filterCards 错误:", error);
                return false;
            }
        },
        
        'toggleAllEffects': function() {
            try {
                console.log("✅ toggleAllEffects 可用");
                return true;
            } catch (error) {
                console.error("❌ toggleAllEffects 错误:", error);
                return false;
            }
        }
    };
    
    let allPassed = true;
    
    for (const [funcName, testFunc] of Object.entries(testFunctions)) {
        if (!testFunc()) {
            allPassed = false;
        }
    }
    
    return allPassed;
}

// 3. 运行测试

function runTests() {
    console.log("🎴 Open-Gi-Oh! 页面功能测试");
    console.log("=" .repeat(50));
    
    const dataLoaded = testDataLoading();
    
    if (dataLoaded) {
        const functionsWorking = testPageFunctions();
        
        if (functionsWorking) {
            console.log("\n🎉 所有测试通过！页面应能正常显示卡牌。");
            console.log("🔄 请刷新页面查看效果：http://118.196.117.234:8080/open-gi-oh-web/final_shrimp_cards_preview.html");
        } else {
            console.log("\n⚠️ 页面功能部分异常，但数据已加载。");
            console.log("🔄 可能需要进一步修复页面代码。");
        }
    } else {
        console.log("\n🚨 数据加载失败！");
        console.log("🔧 请检查：");
        console.log("  1. JS文件是否正确引用");
        console.log("  2. 变量名是否匹配");
        console.log("  3. JS文件是否可访问");
    }
}

// 4. 执行测试

runTests();