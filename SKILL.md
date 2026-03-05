# 🤖 智能一号·如意（AI No.1 Ruyi）Skill

企业级**自然语言交互自动化测试系统**。从 v2.2_suite 升级而来，新增**控制器（Controller）**和**高级调度器（Scheduler）**模块。

---

## 🎯 如意能力全景（v2.2_suite → 如意）

| 模块 | v2.2_suite | 如意（Ruyi） |
|------|------------|--------------|
| **NLP 问答层** | ✅ | ✅ |
| **路径支持** | ✅ | ✅ |
| **有限循环** | ✅ | ✅ |
| **测试报告** | ✅ | ✅ |
| **自动化进化** | ✅ | ✅ |
| **控制器（Controller）** | - | ✅ 统一入口，调度所有模块 |
| **高级调度器（Scheduler）** | - | ✅ 任务依赖图、并发控制 |
| **熔断机制** | - | ✅ 失败快速熔断 |
| **资源隔离** | - | ✅ 指定资源配额 |

---

## 🚀 如意升级亮点

| 能力 | v2.2_suite | 如意 |
|------|------------|------|
| 统一入口 | ❌ 分散调用 | ✅ Controller 统一调度 |
| 任务依赖 | ❌ 无 | ✅ Scheduler 支持依赖图 |
| 并发控制 | ❌ 无 | ✅ 支持最大并发数 |
| 优先级队列 | ❌ 无 | ✅ 支持任务优先级 |
| 熔断机制 | ❌ 无 | ✅ 连续失败 → 熔断跳过 |
| 资源隔离 | ❌ 无 | ✅ 指定时间/内存配额 |
| 自定义插件 | ❌ 无 | ✅ Scheduler 插件化 |

---

## 📋 如意测试流水线（ enhanced）

```
┌─────────────────────────────────────────────────────────────┐
│ 用户输入（自然语言）                                       │
│ "测试这个项目，测 3 次直到成功，超时 120 秒"              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 🎮 控制器（Controller）入口                                │
│ - 接收所有输入                                              │
│ - 意图识别                                                  │
│ - Load plugins                                              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 🎯 高级调度器（Scheduler）                                 │
│ - 解析依赖图（如果有 dependencies=xxx）                   │
│ - 分配资源（时间=120s, 内存=512MB）                       │
│ - 插件链（NLP → Path → Execution → Report → Evolve）     │
│ - 并发控制（max_concurrent=1）                            │
│ - 优先级队列（priority=high/normal/low）                 │
│ - 熔断机制（failures_threshold=3）                        │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 🏗️ 插件链执行（可扩展）                                    │
│ 1️⃣ NLP Plugin: 意图识别 + 实体抽取                        │
│ 2️⃣ Path Plugin: 路径解析 + Shebang 提取                  │
│ 3️⃣ Exec Plugin: 循环执行 + 次数控制                      │
│ 4️⃣ Report Plugin: Markdown 报告生成                     │
│ 5️⃣ Evolve Plugin: 失败 → ai_no1_fix_v2/vN/              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 📊 统一报告 + 进化                                        │
│ - 生成 report_ruyi_*.md                                   │
│ - 追加 MEMORY.md / memory/YYYY-MM-DD.md                   │
│ - 如失败 → ai_no1_fix_ruyi/vN/                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 如意组件集成（enhanced）

| 组件 | 源模块 | 文件路径 | 功能 |
|------|--------|----------|------|
| **Controller** | 如意特有 | `ai_no1_ruyi/controller.py` | 统一入口，调度所有模块 |
| **Scheduler** | 如意特有 | `ai_no1_ruyi/scheduler.py` | 依赖图/并发/熔断/资源 |
| **NLP Plugin** | v2.2 | `ai_no1_v2_2/SKILL.md` | 意图识别 + 实体抽取 |
| **Path Plugin** | v2.1 | `ai_no1_v2_1/SKILL.md` | 路径解析 + Shebang 提取 |
| **Exec Plugin** | v2.0 | `ai_no1_v2/SKILL.md` | 次数/直达/超时/收敛 |
| **Report Plugin** | v2.0 | `ai_no1_v2/reports/` | 统一报告模板 |
| **Evolve Plugin** | v2.0 | `ai_no1_v2/` | 失败 → ai_no1_fix_v2/vN/ |

> ✅ **如意 ≠ 重复实现，只做调度和插件化扩展**

---

## 🛠️ 如意使用方式

### 如意指令格式（自然语言 + 控制器参数）

```
测试 <目标>：
  --次数=N
  --直达=目标
  --超时=N
  --收敛=N
  --verbose                 # 详细模式（每轮输出）
  --skip-confirm            # 跳过追问（直接执行）

  # 如意新增参数
  --concurrent=2            # 最大并发数（默认 1）
  --priority=high           # 任务优先级（high/normal/low）
  --dependencies=/path/to/job1.json  # 依赖图文件
  --timeout-memory=512MB    # 内存配额
  --failures-threshold=3    # 连续失败熔断阈值
```

---

### 示例 1：如意控制 + 熔断

```
用户输入（自然语言）：
  "测试这个项目，测 5 次直到成功，超时 120 秒，连续失败 3 次熔断"
  
如意调度：
  1️⃣ Controller: Load plugins (NLP, Path, Exec, Report, Evolve)
  2️⃣ Scheduler: max_failures=3, reset on success
  3️⃣ NLP Plugin: 提取参数
  4️⃣ Path Plugin: Check existence
  5️⃣ Exec Plugin: Loop 5 times, but break if failures >= 3
  6️⃣ Report: Generate report
```

---

### 示例 2：任务依赖图

```
用户输入：
  "测试服务，依赖 /path/to/prepare.json，并发 2，高优先级"
  
如意调度：
  1️⃣ Scheduler: Load dependencies from prepare.json (graph of tasks)
  2️⃣ Scheduler: max_concurrent=2, priority=high
  3️⃣ Execute tasks in dependency order, up to 2 at a time
  4️⃣ Report: Generate combined report
```

---

### 示例 3：插件化扩展（自定义插件）

```
用户创建插件：
  skills/ai_no1_ruyi/plugins/my_custom_plugin.py
  
如意调度：
  1️⃣ Controller: Scan /plugins/ directory
  2️⃣ Scheduler: Add my_custom_plugin to plugin chain
  3️⃣ Execute: ... → NLP → Path → Exec → MyCustom → Report → Evolve
```

---

## 📊 如意报告增强

| 字段 | v2.2_suite | 如意 |
|------|------------|------|
| **Origin** | /path/app.sh | /path/app.sh |
| **Parsed Name** | app | app |
| **Script Type** | Bash/Python | Bash/Python/Shell/Docker |
| **NLP 原始输入** | ✅ | ✅ |
| **控制器参数** | - | ✅ `concurrent=2, priority=high, ...` |
| **调度器参数** | - | ✅ `dependencies=/path/to/graph.json` |
| **多轮时间线** | ✅ | ✅ |
| **熔断触发** | - | ✅ `failurecount=3 →熔断` |
| **资源配额** | - | ✅ `timeout=120s, memory=512MB` |

---

## 🎯 如意典型场景

| 场景 | 用户输入 | 说明 |
|------|----------|------|
| **基础测试** | `测试 /root/.copaw/bin/copaw` | 自动执行，默认参数 |
| **熔断机制** | `测这个服务，5次，失败3次熔断` | 连续失败 → 跳过后续 |
| **依赖任务** | `测试服务，依赖 prepare.json` | 先执行 prepare，再执行测试 |
| **并发执行** | `测试多个项目，最多3个并发` | 最多 3 个任务一起执行 |
| **插件扩展** | `测试项目，启用 my_plugin` | 自定义插件插入执行链 |

---

## 📄 如意文件结构

```
skills/ai_no1_ruyi/
├── SKILL.md                    ← 核心框架（本文件）
├── controller.py               ← Controller（新增）
├── scheduler.py                ← Scheduler（新增）
├── tools.yml                   ← 工具依赖
├── README.md                   ← 快速上手
├── reports/
│   └── report_ruyi_*.md        ← 统一报告模板
└── plugins/                    ← 插件目录（新增）
    ├── my_custom_plugin.py
    └── ...
```

---

## 🧠 如意核心理念

> **“企业级测试，从一句话开始，到智能调度结束。”**  
>  
> - 统一入口（Controller）  
> - 智能调度（Scheduler：依赖/并发/熔断/资源）  
> - 插件化扩展（可插拔执行链）  
> - 企业级能力（熔断/资源配额/优先级队列）  
> - 自动化进化（失败 → 修复版 Skill）  

---

## 🔄 如意升级路径

| 版本 | 功能 | 状态 |
|------|------|------|
| `ai_no1` | 单次测试 | ✅ |
| `ai_no1_v2` | 有限循环控制 | ✅ |
| `ai_no1_v2_1` | 路径支持 + 本地程序测试 | ✅ |
| `ai_no1_v2_2` | NLP 问答层 | ✅ |
| `ai_no1_v2_2_suite` | 企业级集成 | ✅ 旧版 |
| `ai_no1_ruyi` | **如意**：Controller + Scheduler | ✅ 新版 |

---

> 📌 **智能一号·如意（Ruyi） — 2026-03-05 升级**  
> *-controller-driven test orchestration, scheduler with dependencies/concurrency/circuit-breaker, extensible via plugins*
