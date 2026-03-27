# 🤖 智能一号 v2.1（AI No.1 v2.1）· 快速上手指南

## 🚀 指令格式（支持路径）

```
测试 <路径/命令>：
  --次数=N
  --直达=目标
  --超时=N
  --收敛=N
```

### ✅ 支持所有类型

| 类型 | 示例 | 说明 |
|------|------|------|
| **PATH 命令** | `curl`, `git` | 系统 PATH 中的命令 |
| **绝对路径** | `/usr/local/bin/my_app` | 精确指定可执行文件 |
| **相对路径** | `./my_script.sh` | 当前目录脚本 |
| **Python 脚本** | `python3 my_script.py` | 包含解释器 |
| **Bash 脚本** | `bash /tmp/test.sh` | 指定解释器 |
| **Docker 镜像** | `docker run nginx:latest` | 容器测试 |
| **Shell 串** | `sh test.sh --arg1` | 带参数命令 |

---

## 💡 示例

### 1. 测试本地 Bash 脚本
```
测试 /root/.copaw/scripts/test.sh：
  --次数=3
  --直达=0
  --收敛=2
```
→ 智能一号会自动：
1. 检查 `/root/.copaw/scripts/test.sh` 是否存在  
2. 检查 `test.sh` 是否可执行  
3. 读取 Shebang 判断脚本类型  
4. 生成 5~12 个测试用例  
5. 执行测试 + 收敛检测  

---

### 2. 测试 Python 脚本
```
测试 ./my_python_app.py：
  --次数=5
  --直达=成功
  --超时=120
```

---

### 3. 测试 Docker 容器
```
测试 docker run nginx:latest：
  --次数=2
  --直达=启动成功
  --超时=30
```

---

### 4. 测试通用可执行文件
```
测试 /usr/local/bin/my_app：
  --次数=3
  --直达=exit=0
```

---

## 🔍 预检示例（用户无需手动操作）

| 用户输入 | 智能一号自动完成 |
|----------|------------------|
| `/root/.copaw/scripts/test.sh` | 1. `stat` 检查存在性<br>2. `test -x` 检查可执行性<br>3. `head -1` 读取 Shebang<br>4. 解析脚本功能 |
| `python3 script.py` | 1. 检查 `script.py` 是否存在<br>2. 读取 Shebang `#!/usr/bin/env python3`<br>3. 解析 import 模块依赖 |
| `docker run image:latest` | 1. `docker images` 检查镜像<br>2. 解析 `run` 后的参数 |

---

## 📊 输出报告（v2.1 新增字段）

| 字段 | 说明 |
|------|------|
| `Origin` | 原始路径（如 `/root/.copaw/scripts/test.sh`） |
| `Parsed Name` | 解析后名称（如 `test_script`） |
| `Script Type` | Bash / Python / Go / ... |
| `Shebang` | `#!/bin/bash` 或 `#!/usr/bin/env python3` |
| `Permissions` | `rwxr-xr-x` 或 `❌ 权限不足` |
| `Container Image` | (Docker) 镜像名：`nginx:latest` |

---

## 🔁 退出条件（与 v2.0 相同）

| 条件 | 退出？ |
|------|--------|
| 达到 `--次数` | ✅ 停止 |
| 达到 `--直达` 目标 | ✅ 停止 |
| 超过 `--超时` | ✅ 停止（记录最后一次结果） |
| 达到 `--收敛` | ✅ 停止（认为稳定） |

---

## 🎯 立即测试

输入：
```
测试 /root/.copaw/scripts/test.sh：
  --次数=2
  --直达到=0
```

→ 智能一号 v2.1：
1. 检查 `/root/.copaw/scripts/test.sh` 存在性 + 权限  
2. 提取 Shebang (`#!/bin/bash`)  
3. 生成测试用例（含参数变化、边界条件）  
4. 执行测试（最多 2 轮）  
5. 检查收敛（连续 2 轮结果相同则停）  
6. 生成 `ai_no1_v2_1_report_test_script_*.md`

---

请开始你的指令 🚀  
（支持任何本地程序、脚本、容器）
