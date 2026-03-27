# 🤖 智能一号（AI No.1）· Wget Safe Wrapper v1.0 — 快速使用指南

## 🎯 目的

修复 `wget` 对无效域名时 exit code 不为 `4`（返回 0）的兼容性问题。

---

## 📦 安装

```bash
source /root/.copaw/skills/ai_no1_fix/v1/wget/wget_safe.sh
```

---

## 🧪 用法

### 1. 正常测试（用 `wget_test` 函数）
```bash
wget_test "https://httpbin.org/robots.txt" "httpbin" && echo "✅ OK"
wget_test "http://invalid.invalid.invalid" "bad url" && echo "✅ OK" || echo "❌ 由 wrapper 正确捕获失败"
```

### 2. 自动化流程（用 `set -e`）
```bash
set -e
wget http://invalid.invalid.invalid
echo "如果执行到这里，说明 wget 成功（但实际会失败退出）"
```

---

## 🔧 应急修复（临时修改）

```bash
# 临时启用 strict mode
set -e

# 或显式判断
wget ... || { echo "wget failed!"; exit 1; }
```

---

## 📊 修复前后对比

| 命令 | 修复前 (exit) | 修复后 (exit) |
|------|---------------|---------------|
| `wget http://invalid.invalid.invalid` | `0` | `1`（wrapper 中正确捕获） |
| `wget --spider -q https://...` | `0` | `0` |

---

## 📌 作者

AI No.1 v1.0 Fix Engine (2026-03-05)  
*Fix for issue: wget exit code on DNS failure*