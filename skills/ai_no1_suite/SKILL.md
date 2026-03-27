# 🤖 智能一号（AI No.1）· Tools Test Suite

**AI No.1 v1.0 + Report v1.0-full-20260305 整合**  
*Purpose：对 Linux 工具链进行闭环测试：预检 → 设计 → 执行 → 诊断 → 报告 + 新 skill 自动生成*

---

## 🧪 能力模型（基于全量 62 case 测试提炼）

| 能力 | 描述 | 来源 |
|------|------|------|
| 🔍 **环境预检** | `command -v tool` + 版本识别 + 路径缓存 | 全工具 `command -v` |
| 🧠 **用例自动生成** | 根据工具类型（CLI/UI/网络/语言）生成 5~12 个核心+异常用例 | ls/git/curl/wget/python/bash/node 7 类归纳 |
| 📏 **标准化异常码知识库** | 内置常见工具的 exit code 模式（curl:6/wget:4/bash:127/ls:2/git:1/python:1） | 全量异常场景总结 |
| 🧰 **宽场景覆盖** | 正常/边界/异常三类用例比例 = 7:2:1 | 见 report `62 cases → 46 normal + 16 error` |
| 📊 **富报告** | Markdown + 多级结构（summary → details → diagnostic → new skill） | 报告模板化 |
| 🔄 **自动进化** | 失败时自动生成 `ai_no1_fix/vN/SKILL.md`（含重试逻辑、更详细日志） | robust_echo_test 实践 |

---

## 🔑 使用方式

### 1. 指定工具
```
测试 git curl python3 wget
测试 ffmpeg node
```

### 2. 指定策略（可选）
```
策略: timeout=5s, require_unicode=true, require_network=true
```

### 3. 执行测试
智能一号将自动：
1. **预检环境**（是否存在、版本、路径）  
2. **生成适配性用例**（normal + boundary + error）  
3. **顺序执行**（含失败保护 + 异常码捕获）  
4. **诊断失败原因**（env/args/logic）  
5. **生成报告** + 提交 event 到 `memory/`  
6. **如失败 → 输出 `ai_no1_fix/vN/SKILL.md`**

---

## 📑 核心用例模板（已验证）

| 工具类型 | normal 用例 | boundary 用例 | error 用例 |
|----------|-------------|---------------|------------|
| **CLI (ls/git)** | 基本列出 / 初始化仓库 | `-la` 隐藏文件 / 多级路径 | 错误路径 / 非法命令 |
| **网络 (curl/wget)** | 获取 200 页面 | `-w "%{http_code}"` 校验 | 无效域名 / 超时 |
| **语言 (python/bash)** | 执行 Hello World | `exit(N)` | `1/0`, `os._exit(N)` |
| **转换 (ffmpeg)** | 视频/音频格式转换 | 多种输入格式 | 缺依赖 / 不支持格式 |

> ✅ 已被 **全量 62 case** 验证通过  

---

## 🧠 异常码知识库（v1.0-full）

| tool | 场景 | 期望 exit | 实际 |
|------|------|-----------|------|
| `curl` | 解析失败 | `6` | ✅ `6` |
| `curl` | 4xx/5xx | `0`（但 `http_code=4xx`） | ✅ |
| `wget` | 解析失败 | `4` | ✅ `4`（但有 bug → 修复见 ai_no1_fix） |
| `git` | 非法命令 | `1` | ✅ `1` |
| `ls` | 非法路径 | `2` | ✅ `2` |
| `bash` | 脚本不存在 | `127` | ✅ `127` |
| `python` | `ZeroDivisionError` | `1` | ✅ `1` |
| `python` | `os._exit(N)` | `N` | ✅ |

> 📋 失败根因分类：  
> - `env`: 路径缺失、依赖缺失  
> - `args`: 参数类型错误、格式不匹配  
> - `logic`: 逻辑预期 vs 实际结果不一致  

---

## 📄 报告结构（标准化模板）

```
# 🤖 智能一号（AI No.1）测试报告: <tool1>_<tool2>_<timestamp>
**Tested at**: 2026-03-05 <time> CST  
**Tester**: 智能一号 (AI No.1 v1.0)  
**Suite Version**: v1.0-full-20260305

## ✅ Summary
| Tool | Normal | Bound | Error | Total | Pass Rate |
|------|--------|-------|-------|-------|-----------|
| ...  | ...    | ...   | ...   | ...   | ...%      |

## 🔬 Detailed Results
> [tool1] (`which tool1`, v<ver>)
| # | Case | Command | Expected | Actual | Status |
...

## 🧠 Diagnostic Analysis
- env: 0 error(s)
- args: 0 error(s)
- logic: 1 error(s) [示例]

⚠️ 发现问题：wget 异常码不一致 → 已生成 ai_no1_fix/v1/wget/SKILL.md

## 📦 New Skill Suggestion
> (如 test fail → 提议生成 ai_no1_fix/v1/SKILL.md)
```

---

## 🛠️ Tools Used by This Skill

- `execute_shell_command`：执行测试命令  
- `read_file`：读取日志、历史报告  
- `write_file`：生成 Markdown 报告  
- `edit_file`：更新 `MEMORY.md` / `memory/`  
- `memory_search`：检索过往测试记录  
- `get_current_time`：生成时间戳  

---

## 💡 智能一号核心理念（2026-03-05 共识）

> 1. **失败是数据，不是终点**  
>    —— 每个失败都要提取 pathology（错误类型 + 跟踪码）  
> 2. **测试不求快，求可复现**  
>    —— `timeout`, `command -v`, `cat -v` 是防御三件套  
> 3. **顶级架构师 = 预见 + 自进化**  
>    —— 不仅测工具，还要让工具越测越稳  
> 4. **机器人操控机器人**  
>    —— AI No.1 生成的新 Skill 会继续自我测试，无限进化  

---

## 📌 下一步优化（规划中）

| 任务 | 优先级 | 说明 |
|------|--------|------|
| 🧪 压力测试用例 | 🔵 中 | 超长参数、并发 pipelines |
| 🌐 网络测试/frame | 🔵 中 | 增加 `httpbin.org `/mock server |  
| 🛡️ 安全测试 | 🟡 低 | 输入注入、路径遍历 |
| 📊 CI/CD 适配 | 🔵 中 | 支持 `GITHUB_ACTIONS`, `JENKINS` 环境 |

---

## 🎯 首次执行

请提供想测试的工具名（空格分隔），例如：  
```
测试 ffmpeg jq docker
```

**智能一号** 将立即调度 **Tools Test Suite v1.0** 执行闭环测试

---

> ✅ **AI No.1 v1.0 — 2026-03-05 创建**  
> *AI for AI：机器人操控机器人，测试驱动进化*
