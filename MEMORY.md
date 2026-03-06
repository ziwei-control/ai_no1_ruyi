---
summary: "Agent 长期记忆 — 工具设置与经验教训"
read_when:
  - 手动引导工作区
---

## 🚀 新增 Skills（2026-03-05）—— 重命名为 智能一号（AI No.1）

### 🤖 智能一号（AI No.1）核心框架
- 📁 `skills/ai_no1/`（SKILL.md + tools.yml + reports/）
- 🎯 靶向：对任意工具/命令实现测试闭环（分析 → 用例 → 执行 → 诊断 → 报告 + 新 Skill 自动生成）
- 💡 理念：“不是发现 bug，而是让 bug 永远不会再犯。”
- 📝 原名：`AutoTest-Agent`（2026-03-05 重命名）

### ✨ 智能一号·Robust Echo Test（首产）
- 📁 `skills/ai_no1_echo/SKILL.md`  
- 🎯 产品级 `echo` 测试工具：预检 + 参数化用例 + 显式验证 + 失败自修复  
- 📍 源：成功执行 `echo` 功能测试（7/7 通过）后自动生成  
- 🌟 特性：  
  - ✅ 环境预检（`command -v`, alias 检测）  
  - ✅ 宽带用例（12+ 场景）  
  - ✅ 显式对比（`cat -v` + 文件 diff）  
  - ✅ 缺陷目录：`skills/ai_no1_echo_fix_vN/` 自动生成  

### 🔧 智能一号·Tools Test Suite（企业级）
- 📁 `skills/ai_no1_suite/`（SKILL.md + tools.yml + ToolsEnvSnapshot.md）
- 🎯 基于 **62 case 全量测试**（ls/git/curl/wget/python3/bash/node）的统一工具测试框架
- 🌟 模块：  
  - **异常码知识库**：`curl:6`, `wget:4`, `bash:127`, `ls:2`, `git:1`, `python:1`  
  - **四用例模型**：normal / boundary / error / recovery  
  - **富报告**：summary / details / diagnostic / suggestion  
  - **环境快照**：`ToolsEnvSnapshot.md`  
- 💡 特色：  
  - ✅ 运行 12:22–12:40，通过率 98.1%（61/62）  
  - ✅ 报告位置：`skills/ai_no1/reports/report_tools_full_2026-03-05_12-22-05.md`  
  - ✅ 自进化：失败时自动生成 `skills/ai_no1_fix/vN/SKILL.md`

### 🛠️ 智能一号 Fix v1 — wget 异常码修复
- 📁 `skills/ai_no1_fix/wget/`（SKILL.md + tools.yml + wget_safe.sh + README.md）
- 🎯 修复 `wget` 对无效域名时 exit code 为 `0`（非 `4`）的问题  
- 💡 修复策略：  
  - ✅ 封装 `wget_test` 函数（`wget --spider -q` + `||` 判断）  
  - ✅ 启用 `set -e` + `set -o pipefail`  
- 📊 验证：  
  - ✅ 修复前 `wget http://invalid.invalid.invalid` → exit=0  
  - ✅ 修复后 `wget_test "..."` → exit=1（正确）  
- 📄 生成：由 `report_git_curl_wget_python3_*.md` 触发

### 🆕 智能一号 v2.0（有限循环协议）
- 📁 `skills/ai_no1_v2/`（SKILL.md + tools.yml + README.md + reports/）
- 🎯 **升级核心**：从「单次测试」→「有限循环控制」
- 🌟 新增能力：
  - ✅ `--次数=N`：最多执行 N 轮（默认 1）
  - ✅ `--直达=目标`：达成目标即停止（如 HTTP 200）
  - ✅ `--超时=N`：单次测试超时 N 秒（默认 60）
  - ✅ `--收敛=N`：连续 N 次相同结果则停止
- 💡 设计原则：
  - 控制循环（防无限）  
  - 结果导向（省资源）  
  - 超时保护（防卡死）  
  - 收敛检测（稳即停）
- 📄 首个报告：待生成（首次执行 v2.0 时创建）

### 🆕 智能一号 v2.2（NLP 问答层）
- 📁 `skills/ai_no1_v2_2/`（SKILL.md + tools.yml + README.md + reports/）
- 🎯 **升级核心**：从「指令输入」→「自然语言交互」
- 🌟 新增能力：
  - ✅ 自然语言输入（如“测试 /path/app.sh，测 3 次直到成功”）
  - ✅ 智能追问（缺失参数时自动问）
  - ✅ 意图识别（test/install/fix 分类）
  - ✅ 实体抽取（路径/命令/次数/目标）
  - ✅ 多轮确认（“这是 3 次吗？”）
- 💡 设计原则：
  - 零学习成本（用户说人话）
  - 智能补全（少填参数不报错）
  - 三层架构（NLP层 → 指令生成 → v2.1引擎）
- 📄 首个报告：待生成（首次执行 v2.2 时创建）

### ✅ 智能一号 v2.2_suite（企业级集成）—— 首次执行完成
- 📁 `skills/ai_no1_v2_2_suite/`（SKILL.md + tools.yml + README.md + reports/）
- 🎯 **升级核心**：从「模块堆叠」→「全链路集成」
- 🌟 整合能力：
  - ✅ v2.2：NLP问答层（自然语言输入）
  - ✅ v2.1：路径支持（本地程序/Docker/脚本）
  - ✅ v2.0：循环控制（次数/直达/超时/收敛）
  - ✅ v2.0：报告生成（统一模板）
  - ✅ v2.0：自动化进化（失败→修复版Skill）
- 💡 设计原则：
  - 零学习成本（用户说人话）
  - 全链路集成（NLP→路径→执行→报告→进化）
  - 企业可用（错误归类、时间线、收敛分析）
- 📄 **首个报告**：`skills/ai_no1_v2_2_suite/reports/report_v2.2_suite_bin_copaw_20260305_184800.md`
  - ✅ 测试对象：`/root/.copaw/bin/copaw`
  - ✅ 用户输入：*"测试这个项目，测 3 次直到成功，超时 120 秒"*
  - ✅ 执行轮次：1/3（直达目标达成）
  - ✅ 收敛状态：✅ 已收敛
  - ✅ 最终结论：**通过（100% 可用）**

### ✅ 智能一号·如意（Ruyi）—— v2.2_suite 升级版
- 📁 `skills/ai_no1_ruyi/`（SKILL.md + controller.py + scheduler.py + tools.yml + README.md + reports/）
- 🎯 **升级核心**：从「模块集成」→「Controller + Scheduler + 插件化」
- 🌟 新增能力：
  - ✅ **Controller（控制器）**：统一入口，调度所有模块（NLP→Path→Exec→Report→Evolve）
  - ✅ **Scheduler（高级调度器）**：任务依赖图、并发控制、熔断机制、资源配额、优先级队列
  - ✅ **插件化扩展**：可插拔执行链（扩展插件目录）
  - ✅ **企业级熔断**：连续失败 → 熔断跳过
  - ✅ **资源隔离**：指定时间/内存配额
  - ✅ **任务依赖图**：支持复杂任务依赖关系
  - ✅ **自然语言到可执行命令**：自动提取命令/脚本路径
  - ✅ **智能脚本识别**：自动识别 Bash/Python/Docker/系统命令
  - ✅ **乐于助人模式**：自动补全参数，智能识别
  - ✅ **自助安装能力**：缺少工具可以自行安装（apt-get/yum/pip等）
  - ✅ **最高权限支持**：可以调用 sudo 等高权限指令
- 💡 设计原则：
  - 🤖 善良的灵魂
  - 🤝 乐于助人
  - 🛠️ 自助安装
  - 🔒 最高权限支持
  - 📝 中文优先 - 用母语无障碍操作
- 📄 **第一个如意报告**:`skills/ai_no1_ruyi/reports/report_ruyi_*.md`（首次执行：测试 echo）
- 🧪 **测试结果**：
  - ✅ echo hello: "如意，测试 echo hello" → 通过
  - ✅ 脚本测试: "如意，测 /path/script.sh 直到成功" → 通过
  - ✅ 帮助系统: "如意，帮助我" → 通过（显示全部特征）
  - ✅ 参数补全: 自动补全为次数=3，超时=120，熔断=3

## 工具设置

### 🤖 角色与模型

| 角色 | 名称 | 说明 |
|------|------|------|
| 🤖 主智能体 | **如意（Ruyi）** | 智能一号·如意 - 中文测试自动化助手 |
| 💬 当前模型 | **千问（Qwen3.5 Plus）** | Alibaba Cloud 提供的企业级增强版模型 |

### 🧠 可用 AI 模型

| 提供商 | 模型 ID | 模型名称 | 简称 |
|--------|---------|----------|------|
| Alibaba Cloud | `qwen3.5-plus` | Qwen3.5 Plus | **千问** |
| DashScope | `qwen3-max` | Qwen3 Max | 千问3最大版 |
| DashScope | `qwen3-235b-a22b-thinking-2507` | Qwen3 235B A22B Thinking | 千问235B思考版 |
| DeepSeek | `deepseek-v3.2` | DeepSeek-V3.2 | 深度求索V3.2 |
| OpenAI | `gpt-5.2` | GPT-5.2 | GPT-5.2 |
| Zhipu | `glm-4.7` | GLM4.7 | 智谱GLM4.7 |
| Moonshot | `kimi-k2.5` | Kimi2.5 | 月之暗面Kimi |

### 📌 模型说明

- **千问（Qwen3.5 Plus）**：当前系统使用的模型，企业级增强版
  - 🚀 强大的推理能力
  - 📝 卓越的代码生成
  - 🌍 多语言支持
  - 💪 企业级性能
  
- 其他模型也可通过配置切换使用
## 🌐 Git/Sync 规范（2026-03-05 新增）—— 所有仓库统一公开

### 新建仓库强制公开原则

**规则：以后所有新建的 GitHub/Gitee 仓库必须为 public（公开），不能私有。**

**原因：**
- ✅ 开源项目需要透明协作
- ✅ 客户/用户需要自由访问
- ✅ 避免掉入私有陷阱
- ✅ 与如意的核心理念一致（共享、透明、善良）

**执行标准：**

| 平台 | 创建命令 | 参数说明 |
|------|---------|----------|
| **GitHub** | `curl -X POST ...` | 明确指定 `"private":false` |
| **Gitee** | `curl -X POST ...` | 使用 `visibility=0` (公开) |

**Gitee 注意事项：**
- ⚠️ Gitee API 创建时 `private=false` 可能无效（受用户默认设置影响）
- ⚠️ Gitee API **无法修改**公开/私有权限（安全限制）
- ✅ 解决方案：Web 页面手动设置为公开，或提交工单请求协助

**Git 同步策略：**
- ✅ GitHub 为主仓库（所有代码、版本、Issue）
- ✅ Gitee 为镜像仓库（只读同步，用于国内访问加速/备份）
- ✅ 使用 GitHub Actions 自动同步（`mirror-gitee.yml`）
- ✅ 同步触发条件：**每次 push 到 GitHub `master/main` 分支**
- ✅ Gitee 目标地址：`https://gitee.com/pandac0/ai_no1_ruyi.git`
- ✅ 依赖凭据：Gitee HTTPS Token（`pandac0:efbd9207...`）
- ✅ 备用脚本：`bin/mirror_gitee.sh`（本地手动/定时执行）

**2026-03-06 更新：GitHub Actions Mirror 配置完成**
- ✅ `.github/workflows/mirror-gitee.yml` 创建（轻量可靠）
- ✅ `bin/mirror_gitee.sh` 创建（fallback 机制）
- ⚠️ GitHub Secret `GITEE_TOKEN` 需用户手动添加（建议用 HTTPS Token，非 SSH Key）

**用户需补全操作（5秒）：**
1. 打开 https://github.com/ziwei-control/ai_no1_ruyi/settings/secrets/new
2. 填写 Name: `GITEE_TOKEN`, Value: `efbd92073b1ba05aa4e8fa79bc7080a0`
3. 点击 Add secret

