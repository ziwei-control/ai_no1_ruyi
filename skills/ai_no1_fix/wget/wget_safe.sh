set -e

# 修复核心：启用 strict mode
set -o pipefail

wget_test() {
    local url="$1"
    local name="$2"
    echo "=== AI No.1 [wget_safe] Testing: $name ==="
    if wget --spider -q "$url" 2>/dev/null; then
        echo "✅ $name:可连接"
        return 0
    else
        echo "❌ $name:失败 (exit $(echo $?))"
        return 1
    fi
}

# 测试 1：无效域名（应失败）
wget_test "http://invalid.invalid.invalid" "invalid URL" || echo "✅ AI No.1 无效域名测试通过（exit 非0）"

# 测试 2：有效站点（应成功）
wget_test "https://httpbin.org/robots.txt" "httpbin" || echo "❌ AI No.1 httpbin 测试失败"

echo "=== AI No.1 Wget Safe Test Finished ==="