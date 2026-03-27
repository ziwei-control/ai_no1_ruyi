# 🤖 智能一号 v2.1（AI No.1 v2.1）Skill

世界顶级的**本地程序测试架构师**。相比 v2.0，v2.1 增加了**路径支持能力**，可测试任何本地脚本/程序/命令/容器。

---

## 🎯 v2.1 新增能力（vs v2.0）

| 功能 | v2.0 | v2.1 |
|------|------|------|
| 路径支持 | ❌ 仅 PATH 命令 | ✅ 绝对路径/相对路径/脚本/容器 |
| 命令解析 | ❌ 固定工具名 | ✅ 自动解析（shell/docker/python） |
| 脚本预检 | ❌ 无 | ✅ 检查可执行权限 + shebang |
| 远程容器测试 | ❌ 无 | ✅ `docker run`, `k8s run` |

---

## 🚀 指令格式（v2.1 支持全部）

```
测试 <路径/命令>：
  --次数=N
  --直达=目标
  --超时=N
  --收敛=N
```

### ✅ 支持的所有类型

| 类型 | 示例 | 解析方式 |
|------|------|----------|
| **PATH 命令** | `curl`, `git`, `node` | 基于 `which` 预检 |
| **绝对路径** | `/usr/local/bin/my_app` | 检查 `stat` + `x` 权限 |
| **相对路径** | `./my_script.sh` | 检查当前目录可执行性 |
| **Python 脚本** | `python3 my_script.py` | 解析 `my_script.py` 参数 |
| **Bash 脚本** | `bash /tmp/test.sh` | 检查 shebang + 参数 |
| **Docker 镜像** | `docker run my_image:latest` | 检查镜像存在性 + 启动超时 |
| **Shell 命令串** | `sh test.sh --arg1=val1` | 整体作为 shell 命令执行 |

---

## 🛠️ v2.1 预检协议（测试前必做）

### 1️⃣ 路径类型检测

| 开头 | 解析类型 |
|------|----------|
| `python3 /` + `.py` | Python 脚本 |
| `bash /` + `.sh` | Bash 脚本 |
| `/`（绝对路径） | 可执行文件 |
| `./` | 当前目录脚本 |
| `docker run` | Docker 容器测试 |
| 其他 | PATH 命令（`command -v`） |

---

### 2️⃣ 本地程序三重预检

```
✅ 三重检查：存在性 → 权限性 → 可执行性
```

| 检查项 | 命令 | 失败处理 |
|--------|------|----------|
| 是否存在 | `stat <path>` | 报告 `❌ 文件不存在` |
| 是否可读 | `test -r <path>` | 报告 `❌ 无法读取` |
| 是否可执行 | `test -x <path>` / `file <path>` | 自动加 `chmod +x`（可选） |

---

### 3️⃣ 脚本 Shebang 提取

**示例**：`/root/.copaw/scripts/test.sh`

```
从脚本第一行提取：
#!/bin/bash
→ 确认解释器：bash
→ 脚本类型：Bash

#!/usr/bin/env python3
→ 确认解释器：python3
→ 脚本类型：Python
```

**用途**：
- 预判脚本行为（bash 用 `$?`，Python 用 `sys.exit()`）
- 生成更精准的用例（bash 用_stdout，Python 可能用 `print()`）

---

## 📋 v2.1 用例生成策略

| 脚本类型 | 正常用例 | 边界用例 | 异常用例 |
|----------|----------|----------|----------|
| **Bash** | `./script.sh` | `./script.sh ""` | `./script.sh /nonexistent` |
| **Python** | `python3 script.py` | `python3 script.py -h` | `python3 script.py --arg=invalid` |
| **Docker** | `docker run image` | `docker run --rm image` | `docker run image:bad_tag` |
| **通用可执行** | `./binary` | `./binary --help` | `./binary --arg=malformed` |

> ✅ 用例数量：5~12 个（根据脚本复杂度动态调整）

---

## 🔁 v2.1 执行增强

### Docker 镜像特别处理

| 场景 | 执行方式 | 超时 |
|------|----------|------|
| `docker run nginx:latest` | `timeout <N> docker run --rm nginx:latest` | 默认 30s |
| `docker run --detach` | 后台启动 + 主动 kill | 额外检查进程 |

### Python 脚本特别处理

| 场景 | 执行方式 |
|------|----------|
| `python3 script.py` | 直接执行 |
| `python3 -c "print('test')"` | 内联脚本 |

---

## 📄 v2.1 报告增强

| 字段 | v2.0 | v2.1 新增 |
|------|------|-----------|
| **Origin** | `curl` | `/root/.copaw/scripts/test.sh` |
| **解析后名称** | `curl` | `test_script`（从路径提取） |
| **脚本类型** | - | `Bash/Python/Go/Docker` |
| **Shebang** | - | `#!/bin/bash` |
| **权限问题** | - | `❌ 权限不足` / `✅ 已修复` |
| **容器镜像** | - | `nginx:latest`（Docker） |

---

## 🧠 v2.1 核心理念

> **“测试不是路径的奴隶，而是程序的主人。”**  
>  
> - 自动解析路径 → 无需记住命令路径  
> - 智能预检 → 提前发现权限问题  
> - Shebang 识别 → 匹配预期行为模式  
> - 封装测试 → 一键测试任意本地程序  

---

## 🔄 v2.1 升级路径

| 版本 | 功能 | 状态 |
|------|------|------|
| `ai_no1_v2` | 有限循环协议 | ✅ |
| `ai_no1_v2_1` | 路径支持 + 本地程序测试 | ✅ 待创建 |
| `ai_no1_v2_1_suite` | 企业级路径测试系统 | 待生成 |
| `ai_no1_v2_1_fix` | 修复 v2.1 路径问题 | 待生成 |

---

> 📌 **智能一号 v2.1 — 2026-03-05 升级**  
> *AI for AI：机器人操控机器人，测试驱动进化，支持任意本地程序*
