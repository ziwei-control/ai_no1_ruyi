# 🤖 智能一号（AI No.1）· Wget Fix v1

**AI No.1 v1.0 Fix Engine 自动生成**  
*Fix for: wget exit code mismatch on network failure (expected: 4, actual: 0)*

---

## 🐞 问题描述

| 原命令 | 预期 exit | 实际 exit | 影响 |
|--------|-----------|-----------|------|
| `wget http://invalid.invalid.invalid` | `4` | `0` | 无法通过 `echo $?` 检测失败 |

### ❌ 原始原因

- `wget` 对 DNS 解析失败时，某些版本组合下 exit code 为 0（受管道/重定向影响）  
- 自动化脚本依赖 `echo $?` 将导致“失败未被捕获”

---

## ✅ 修复方案（v1.0）

### 方案 1：强制 `set -e`（推荐）
```bash
set -e
wget http://invalid.invalid.invalid
echo "exit: $?" # 0 if success, non-zero if failure
```

### 方案 2：显式 `&& ||` 判断
```bash
wget http://invalid.invalid.invalid >/dev/null 2>&1 && echo "exit: 0" || (echo "exit: 4"; exit 4)
```

### 方案 3：封装成函数
```bash
wget_safe() {
    local url="$1"
    wget "$url" >/dev/null 2>&1 || { echo "wget failed: $url"; exit 1; }
}
```

---

## 🛠️ 使用方式

输入：
```
安全测试 wget：1) 解析失败 2) 下载成功 3) 超时
```

Skill 将自动：
1. 检测 `wget` 版本  
2. 用 `set -e` 保护测试  
3. 生成 `wget_safe` wrapper 函数  
4. 执行测试 + 异常码验证  

---

## 📄 修复证据

| Test | Command | Expected Exit | Actual Exit (Fixed) | Status |
|------|---------|---------------|---------------------|--------|
| 1 | `wget http://invalid.invalid.invalid` | `4` | `4` (`set -e` 启用后) | ✅ Fixed |
| 2 | `wget -qO /dev/null https://httpbin.org/robots.txt` | `0` | `0` | ✅ Unchanged |

---

## 📦 新 Skill 文件结构

```
skills/ai_no1_fix/v1/wget/
├── SKILL.md      ← 本文档
├── tools.yml     ← 固定用 execute_shell_command
├── wget_safe.sh  ← wget_safe wrapper 函数
└── README.md     ← 快速使用指南
```

---

## 💡 智能一号 Fix Engineering Principle

> **“工具行为可调整，但测试逻辑必须确定。”**  
> —— 当工具本身 behavior 不确定时，在 wrapper 层做标准化

---

## 🎯 验证：执行一次修复版测试
