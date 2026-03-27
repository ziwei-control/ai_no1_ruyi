# 微信公众号文章存档

## 文章信息

**标题：** OpenClaw 玩家有福了！开源 Dashboard 来了，一屏看全所有机器人状态还能养像素人

**链接：** https://mp.weixin.qq.com/s/fr9vs8pEc8wRGcwKhtMgOw

**获取时间：** 2026-03-22

**获取状态：** ⚠️ 部分内容（因微信反爬虫机制，无法直接获取完整原文）

---

## 文章核心内容（基于相关 GitHub 项目整理 + 部分原文提取）

### 🎯 主要内容概述

这篇文章介绍了一个开源的 **OpenClaw Dashboard** 项目，这是一个用于监控和管理 OpenClaw AI 代理的可视化控制面板。

从原文提取到的关键信息：
- 文章提到了 **OpenClaw-bot-review** 项目
- 提供了 GitHub 克隆命令：`git clone https://github.com/xmanrui/OpenClaw-bot-review.git`
- 安装步骤：`cd OpenClaw-bot-review` → `npm install` → `npm run dev`
- 访问地址：`http://localhost:3000`
- 提供了 Docker 部署方案
- 包含 dashboard.png 和 Pixel Office 的截图

### ✨ 核心功能特性

#### 1. **会话管理**
- 查看所有代理会话
- 实时活动状态监控
- 会话搜索和过滤

#### 2. **监控和统计**
- **Rate Limit 监控** - 跟踪 Claude 和 Gemini API 使用情况
- **成本分析** - 按模型、会话和时间段详细分解支出
- **实时动态** - 跨所有会话的代理消息实时流
- **活动热力图** - 可视化过去 30 天的使用高峰时段
- **连续追踪** - 监控每日活动连续记录

#### 3. **内存和文件管理**
- **内存查看器** - 浏览和读取代理内存文件（MEMORY.md、HEARTBEAT.md、每日笔记）
- **文件管理器** - 查看和编辑工作区文件、技能和配置

#### 4. **系统健康监控**
- CPU、RAM、磁盘、温度监控
- 24 小时健康历史火花图
- 系统健康仪表板

#### 5. **服务控制**
- 快速操作重启 OpenClaw、仪表板或其他服务
- 日志查看器 - 实时系统日志自动刷新
- Cron 管理 - 查看、启用/禁用和手动触发 cron 任务

#### 6. **集成和扩展**
- **Tailscale 集成** - 查看 Tailscale 状态、IP 和连接的对等点
- **Docker 管理** - 查看容器、镜像、系统使用情况
- **Git 活动** - 跟踪跨仓库的最近提交
- **通知中心** - 审计日志事件源

#### 7. **安全特性**
- **用户名/密码认证** - 安全的注册和 PBKDF2 密码哈希
- **TOTP MFA** - 可选的双因素认证（Google Authenticator 兼容）
- **安全加固** - HSTS、CSP、速率限制、定时安全比较、审计日志

### 🚀 技术栈

- **前端：** HTML, CSS, JavaScript (TypeScript)
- **后端：** Node.js v18+
- **特点：** 纯 Node.js 实现，无需数据库或 npm 包
- **依赖：** 最小化依赖

### 📦 安装方式

#### 方法一：OpenClaw-bot-review（原文推荐）

根据从原文提取的信息：

```bash
# 克隆仓库
git clone https://github.com/xmanrui/OpenClaw-bot-review.git

# 进入目录
cd OpenClaw-bot-review

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 访问 http://localhost:3000
```

#### 方法二：通用 Dashboard 安装
```bash
# 克隆仓库
git clone https://github.com/tugcantopaloglu/openclaw-dashboard.git
cd openclaw-dashboard

# 设置 OpenClaw 工作区路径（可选，自动检测）
export WORKSPACE_DIR=/path/to/your/openclaw/workspace

# 启动仪表板
node server.js

# 访问 http://localhost:7000
```

#### Docker 部署
```bash
# 构建
docker build -t openclaw-dashboard .

# 运行
docker run -d \
  --name openclaw-dashboard \
  -p 3001:3001 \
  -e WORKSPACE_DIR=/app/workspace \
  -e DASHBOARD_ALLOW_HTTP=true \
  -v ~/.openclaw:/home/node/.openclaw:ro \
  -v ~/.openclaw/workspace:/app/workspace \
  openclaw-dashboard
```

### 🎨 界面特性

- **深色/浅色主题** - 在深色和浅色模式之间切换
- **键盘快捷键** - 使用热键快速导航（1-7、Space、/、Esc、?）
- **移动响应式** - 适用于手机和平板电脑
- **浏览器通知** - 在使用限制接近时获得提醒

### 🛡️ 安全功能

- PBKDF2 密码哈希（100,000 次迭代，SHA-512，随机盐）
- 定时安全比较 - 防止定时攻击
- 服务器端会话 - 会话令牌存储在内存中
- 速率限制 - 5 次失败尝试软锁定 15 分钟，20 次硬锁定
- HTTPS 强制 - 除 localhost 和 Tailscale 外
- 安全头：HSTS、CSP、X-Frame-Options 等
- 审计日志 - 所有认证事件和破坏性操作记录

### 🌐 网络安全

**推荐访问方式：**
1. **Localhost** - 同一机器访问：`http://localhost:7000`
2. **Tailscale** - Tailscale 网络访问：`http://100.x.x.x:7000`
3. **本地网络** - LAN 访问（使用 HTTPS 或设置环境变量）

**不建议暴露在公共互联网** - 设计用于私有网络

### 📊 相关 GitHub 项目

根据搜索，有多个相关的 OpenClaw Dashboard 项目：

1. **tugcantopaloglu/openclaw-dashboard** - 530 stars
   - 安全、实时监控仪表板
   - 认证、TOTP MFA、成本跟踪、实时源、内存浏览器等

2. **abhi1693/openclaw-mission-control** - 2.9k stars
   - AI 代理编排仪表板
   - 管理 AI 代理、分配任务、协调多代理协作

3. **grp06/openclaw-studio** - 1.8k stars
   - 简洁的 OpenClaw Web 仪表板
   - 连接 Gateway、管理代理

4. **mudrii/openclaw-dashboard** - 309 stars
   - 美观、零依赖的 AI 代理指挥中心
   - Python 实现

5. **xmanrui/OpenClaw-bot-review** - 870 stars
   - 轻量级 Web 仪表板
   - 查看所有 OpenClaw 机器人/代理/模型/会话状态

6. **1186258278/OpenClawChineseTranslation** - 3.4k stars
   - OpenClaw 汉化版
   - CLI + Dashboard 全中文支持

### 🎁 生态系统工具

#### ClawPanel
- 内置 AI 助手的 OpenClaw 可视化管理面板
- AI 助手、图片识别、一键安装、可视化管理

#### ClawApp
- 手机端聊天客户端
- 流式聊天、图片收发、工具调用、PWA + APK

### 💡 文章提到的"养像素人"功能

虽然无法获取完整原文，但根据标题和上下文推测：
- 可能是指仪表板中的**像素风格可视化**或**虚拟宠物**功能
- 可能与**活动热力图**、**连续追踪**等游戏化元素相关
- 可能是某种**代理状态可视化**的创意展示方式

---

## 技术限制说明

### ⚠️ 获取困难原因

1. **微信反爬虫机制**
   - 检测到自动化访问环境
   - 触发"环境异常"安全验证
   - 需要人工交互验证码

2. **动态内容加载**
   - 主要内容通过 JavaScript 动态加载
   - 简单的 HTTP 请求无法获取完整内容

3. **访问限制**
   - 多个内容提取服务（r.jina.ai、archive.org 等）均无法绕过
   - Google 缓存、Bing 缓存等均不可用

### ✅ 已获取的信息

- ✅ 文章标题
- ✅ 文章主题（OpenClaw 开源 Dashboard）
- ✅ 相关 GitHub 项目信息
- ✅ 功能特性详情
- ✅ 安装和使用说明

### 📝 建议

如需获取完整原文，建议：
1. 直接在微信中打开链接阅读
2. 手动复制文章内容
3. 联系文章作者获取原文

---

## 档案创建信息

**创建时间：** 2026-03-22
**创建者：** 如意 (Ruyi) - AI No.1
**目的：** 固化微信文章内容，避免后续无法访问
**状态：** 部分完成（基于相关项目信息整理）

---

## 参考资料

- GitHub: https://github.com/tugcantopaloglu/openclaw-dashboard
- GitHub: https://github.com/1186258278/OpenClawChineseTranslation
- OpenClaw 官网：https://openclaw.ai/
- 汉化官网：https://openclaw.qt.cool/
