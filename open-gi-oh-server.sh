#!/bin/bash
# 🎴 Open-Gi-Oh! 专属HTTP服务器启动脚本
# 使用专属端口 18890，与现有8080服务器完全分离

PORT=18890
DIR="/root/.openclaw/workspace/open-gi-oh-web"
LOG_FILE="/tmp/open-gi-oh-server-18890.log"

echo "🎴 Open-Gi-Oh! 专属HTTP服务器启动..."
echo "📁 工作目录: $DIR"
echo "🌐 端口: $PORT"
echo "📝 日志文件: $LOG_FILE"
echo "---"

# 检查端口是否被占用
if netstat -tln 2>/dev/null | grep -q ":$PORT "; then
    echo "❌ 端口 $PORT 已被占用，尝试停止现有进程..."
    lsof -ti:$PORT 2>/dev/null | xargs kill -9 2>/dev/null
    sleep 2
fi

# 进入工作目录
cd "$DIR"

# 启动HTTP服务器
echo "🚀 启动Open-Gi-Oh!专属HTTP服务器..."
echo "   🌐 访问链接: http://118.196.117.234:$PORT/"
echo "   🦐 虾虾卡牌: http://118.196.117.234:$PORT/shrimp_cards_preview.html"
echo "   🎮 完整演示: http://118.196.117.234:$PORT/open-gi-oh-complete-demo.html"
echo "---"

# 启动服务器（后台运行）
python3 -m http.server $PORT --bind 0.0.0.0 > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# 等待服务器启动
sleep 3

# 检查是否启动成功
if netstat -tln 2>/dev/null | grep -q ":$PORT "; then
    echo "✅ Open-Gi-Oh!专属服务器启动成功！"
    echo "📊 服务器信息:"
    echo "   PID: $SERVER_PID"
    echo "   端口: $PORT"
    echo "   目录: $DIR"
    echo "   🌐 主入口: http://118.196.117.234:$PORT/"
    echo "---"
    echo "🔧 停止服务器: kill $SERVER_PID"
    echo "📋 查看日志: tail -f $LOG_FILE"
    echo "🎴 系统暴君宣言：专属服务器，干净整洁！🔥"
else
    echo "❌ 服务器启动失败！"
    echo "💡 可能的原因："
    echo "   1. 端口 $PORT 被防火墙阻止"
    echo "   2. Python环境问题"
    echo "   3. 权限不足"
    echo "🔧 解决方案："
    echo "   - 尝试其他端口（如 18891, 18892）"
    echo "   - 检查防火墙设置"
    echo "   - 使用sudo运行（如果需要）"
    kill $SERVER_PID 2>/dev/null
fi