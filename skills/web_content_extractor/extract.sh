#!/bin/bash

# Web Content Extractor Script
# 网页内容提取器 - 实现 SKILL.md 中描述的功能

# 配置
WORKING_DIR="${WORKING_DIR:-/root/.copaw}"
MEMORY_DIR="$WORKING_DIR/memory"
TIMEOUT_SHORT=30
TIMEOUT_LONG=60
TIMEOUT_XLONG=90

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 确保 memory 目录存在
mkdir -p "$MEMORY_DIR"

# 生成存档文件名
generate_filename() {
    local url="$1"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local domain=$(echo "$url" | sed -e 's|^[^/]*//||' -e 's|/.*$||' | tr '.' '_' | tr '-' '_')
    echo "${MEMORY_DIR}/web_archive_${domain}_${timestamp}.md"
}

# 方法 1: 使用 r.jina.ai API
try_jina_ai() {
    local url="$1"
    log_info "方法 1: 尝试 r.jina.ai API..."
    
    local result=$(timeout $TIMEOUT_LONG curl -s --max-time $TIMEOUT_LONG \
        "https://r.jina.ai/http://$(echo $url | sed 's|^https\?://||')" 2>&1) || true
    
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        # 检查是否是错误页面
        if echo "$result" | grep -q "环境异常\|CAPTCHA\|404\|not found"; then
            log_warning "r.jina.ai 触发验证或错误"
            return 1
        fi
        
        # 检查是否获取到内容
        if [ ${#result} -gt 100 ]; then
            log_success "r.jina.ai 成功提取"
            echo "$result"
            return 0
        fi
    fi
    
    log_warning "r.jina.ai 失败"
    return 1
}

# 方法 2: curl 模拟移动端
try_curl_mobile() {
    local url="$1"
    log_info "方法 2: 尝试 curl 模拟移动端..."
    
    local result=$(timeout $TIMEOUT_XLONG curl -s \
        -A "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36" \
        -H "Accept: text/html,application/xhtml+xml" \
        -H "Accept-Language: zh-CN,zh;q=0.9" \
        -H "Referer: https://mp.weixin.qq.com/" \
        --compressed \
        --max-time $TIMEOUT_XLONG \
        "$url" 2>&1) || true
    
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        if [ ${#result} -gt 500 ]; then
            log_success "curl 获取到 HTML 内容"
            echo "$result"
            return 0
        fi
    fi
    
    log_warning "curl 失败"
    return 1
}

# 方法 3: 尝试 GitHub 搜索相关内容
try_github_search() {
    local url="$1"
    local keywords="$2"
    log_info "方法 3: 尝试 GitHub 搜索相关项目..."
    
    local result=$(timeout $TIMEOUT_LONG curl -s --max-time $TIMEOUT_LONG \
        "https://r.jina.ai/http://github.com/search?q=$(echo "$keywords" | sed 's/ /+/g')" 2>&1) || true
    
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        if echo "$result" | grep -q "Repository\|stars"; then
            log_success "GitHub 搜索成功"
            echo "$result"
            return 0
        fi
    fi
    
    log_warning "GitHub 搜索失败"
    return 1
}

# 从 HTML 提取文本
extract_text_from_html() {
    local html="$1"
    
    # 提取标题
    local title=$(echo "$html" | grep -oP '<title>\K[^<]+' | head -1 || echo "未知标题")
    
    # 提取段落（简单版本）
    local paragraphs=$(echo "$html" | strings | grep -oP '>[^<]{20,200}<' | \
        sed 's/^>//; s/<$//' | head -50)
    
    echo "## 提取的文本内容"
    echo ""
    echo "$paragraphs"
}

# 创建档案文件
create_archive() {
    local url="$1"
    local content="$2"
    local method="$3"
    local status="$4"
    local extra_info="$5"
    
    local filename=$(generate_filename "$url")
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$filename" << EOF
# 网页内容存档

## 元数据
- **URL：** $url
- **提取时间：** $timestamp
- **提取方法：** $method
- **状态：** $status

---

## 正文内容

$content

---

$extra_info

## 技术信息
- 生成时间：$timestamp
- 存档位置：$filename

---

**备注：** 此档案由 Web Content Extractor Skill 自动生成
EOF
    
    echo "$filename"
}

# 主函数
main() {
    if [ -z "$1" ]; then
        log_error "请提供 URL 参数"
        echo "用法：$0 <URL> [关键词]"
        exit 1
    fi
    
    local url="$1"
    local keywords="${2:-}"
    
    log_info "开始提取网页内容..."
    log_info "URL: $url"
    echo ""
    
    local content=""
    local method=""
    local status=""
    local extra_info=""
    
    # 尝试方法 1: r.jina.ai
    content=$(try_jina_ai "$url")
    if [ $? -eq 0 ]; then
        method="r.jina.ai API"
        status="✅ 成功"
    else
        # 尝试方法 2: curl 移动端
        local html=$(try_curl_mobile "$url")
        if [ $? -eq 0 ]; then
            method="curl 移动端模拟"
            status="⚠️ 部分成功 (HTML)"
            content=$(extract_text_from_html "$html")
            
            # 如果有额外关键词，尝试 GitHub 搜索补充
            if [ -n "$keywords" ]; then
                local github_result=$(try_github_search "$url" "$keywords")
                if [ $? -eq 0 ]; then
                    extra_info="## 相关项目信息\n\n从 GitHub 获取的补充信息：\n\n$github_result"
                    status="⚠️ 部分成功 (HTML + GitHub)"
                fi
            fi
        else
            # 尝试方法 3: GitHub 搜索
            if [ -n "$keywords" ]; then
                local github_result=$(try_github_search "$url" "$keywords")
                if [ $? -eq 0 ]; then
                    method="GitHub 搜索"
                    status="⚠️ 仅获取到相关项目"
                    content="# 相关项目信息\n\n$github_result"
                else
                    method="全部方法"
                    status="❌ 失败"
                    content="无法提取内容，所有方法均失败"
                    extra_info="## 尝试记录\n\n1. r.jina.ai - 触发验证\n2. curl - 无法获取\n3. GitHub 搜索 - 无结果\n\n## 建议\n\n建议用户手动访问链接并复制内容"
                fi
            else
                method="全部方法"
                status="❌ 失败"
                content="无法提取内容，所有方法均失败"
                extra_info="## 尝试记录\n\n1. r.jina.ai - 触发验证\n2. curl - 无法获取\n\n## 建议\n\n建议用户手动访问链接并复制内容，或提供关键词以便搜索相关项目"
            fi
        fi
    fi
    
    # 创建档案
    local filename=$(create_archive "$url" "$content" "$method" "$status" "$extra_info")
    
    echo ""
    log_success "提取完成！"
    echo ""
    echo "📄 存档位置：$filename"
    echo "📊 提取方法：$method"
    echo "📋 状态：$status"
    echo ""
    
    # 显示前几行内容预览
    echo "📖 内容预览："
    echo "---"
    head -20 "$filename"
    echo "---"
    echo ""
    echo "完整内容请查看：$filename"
}

# 执行主函数
main "$@"
