#!/bin/bash

# Open-Gi-Oh! 网页部署脚本
# 版本: 1.0.0
# 作者: 凤丹 (Feng Dan) - 系统暴君

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
PORT=${1:-8080}
TARGET_DIR=${2:-"./web_files"}
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}🎴 Open-Gi-Oh! 网页部署脚本${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "版本: 1.0.0"
    echo -e "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "系统: $(uname -s)"
    echo ""
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    print_info "检查系统依赖..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        print_success "✅ Python3 已安装"
    else
        print_error "❌ Python3 未安装"
        exit 1
    fi
    
    # 检查HTTP服务器
    if command -v python3 -m http.server --help &> /dev/null; then
        print_success "✅ Python HTTP服务器 可用"
    else
        print_error "❌ Python HTTP服务器 不可用"
        exit 1
    fi
    
    # 检查curl
    if command -v curl &> /dev/null; then
        print_success "✅ curl 已安装"
    else
        print_warning "⚠️ curl 未安装，部分功能可能受限"
    fi
}

validate_web_files() {
    print_info "验证网页文件..."
    
    REQUIRED_FILES=(
        "final_shrimp_cards_preview.html"
        "advanced_shrimp_cards.js"
        "shrimp_formulas.json"
        "index.html"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [[ -f "$TARGET_DIR/$file" ]]; then
            print_success "✅ $file 存在"
        else
            print_error "❌ $file 不存在"
            exit 1
        fi
    done
    
    # 检查文件大小
    total_size=$(du -sh "$TARGET_DIR" | cut -f1)
    print_info "网页文件总大小: $total_size"
}

start_http_server() {
    print_info "启动HTTP服务器..."
    
    # 检查端口是否被占用
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_error "❌ 端口 $PORT 已被占用"
        exit 1
    fi
    
    # 启动服务器
    print_info "在端口 $PORT 启动HTTP服务器..."
    print_info "访问地址: http://localhost:$PORT"
    print_info "演示页面: http://localhost:$PORT/index.html"
    
    # 后台启动服务器
    python3 -m http.server $PORT --directory "$TARGET_DIR" > server.log 2>&1 &
    SERVER_PID=$!
    
    # 保存PID
    echo $SERVER_PID > server.pid
    
    # 等待服务器启动
    sleep 2
    
    # 验证服务器运行
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/ > /dev/null 2>&1; then
        print_success "✅ HTTP服务器启动成功 (PID: $SERVER_PID)"
        print_info "服务器日志: $BASE_DIR/server.log"
    else
        print_error "❌ HTTP服务器启动失败"
        exit 1
    fi
}

deploy_to_external() {
    print_info "部署到外部服务器..."
    
    # 这里可以添加外部服务器部署逻辑
    # 例如：SCP到远程服务器、上传到CDN等
    
    print_info "当前部署位置: $TARGET_DIR"
    print_info "外部部署功能未启用，如需启用请修改脚本"
}

cleanup() {
    print_info "清理资源..."
    
    if [[ -f server.pid ]]; then
        SERVER_PID=$(cat server.pid)
        if kill -0 $SERVER_PID 2>/dev/null; then
            print_info "停止HTTP服务器 (PID: $SERVER_PID)..."
            kill $SERVER_PID
            wait $SERVER_PID 2>/dev/null
            print_success "✅ HTTP服务器已停止"
        fi
        rm -f server.pid
    fi
    
    if [[ -f server.log ]]; then
        rm -f server.log
    fi
}

show_help() {
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -p, --port <端口>      设置HTTP服务器端口 (默认: 8080)"
    echo "  -d, --dir <目录>       设置网页文件目录 (默认: ./web_files)"
    echo "  -e, --external         启用外部服务器部署"
    echo "  -h, --help             显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                     使用默认设置启动"
    echo "  $0 -p 3000 -d ./dist   使用自定义设置启动"
    echo "  $0 -e                  启用外部部署"
}

main() {
    # 处理命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--port)
                PORT="$2"
                shift 2
                ;;
            -d|--dir)
                TARGET_DIR="$2"
                shift 2
                ;;
            -e|--external)
                DEPLOY_EXTERNAL=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                print_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 确保目录存在
    mkdir -p "$TARGET_DIR"
    
    print_header
    check_dependencies
    validate_web_files
    
    # 设置退出时清理
    trap cleanup EXIT
    
    start_http_server
    
    if [[ "$DEPLOY_EXTERNAL" == "true" ]]; then
        deploy_to_external
    fi
    
    print_success "🎉 Open-Gi-Oh! 网页部署完成！"
    echo ""
    echo -e "${GREEN}📊 部署信息${NC}"
    echo -e "端口: $PORT"
    echo -e "目录: $(realpath "$TARGET_DIR")"
    echo -e "主页面: http://localhost:$PORT/index.html"
    echo -e "最终版卡牌: http://localhost:$PORT/final_shrimp_cards_preview.html"
    echo ""
    echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
    
    # 保持脚本运行
    wait $SERVER_PID
}

# 运行主函数
main "$@"