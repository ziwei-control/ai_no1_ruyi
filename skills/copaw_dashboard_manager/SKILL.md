# CoPaw Dashboard Manager 技能

## 📖 技能描述

**CoPaw Dashboard 管理器** - 用于管理和访问 OpenClaw-bot-review Dashboard 的适配技能。

## 🎯 功能

### 1. Dashboard 控制

- **启动 Dashboard**
  ```bash
  cd /root/.copaw/OpenClaw-bot-review
  npm run dev
  ```

- **停止 Dashboard**
  ```bash
  pkill -f "npm run dev"
  ```

- **检查状态**
  ```bash
  curl -s http://localhost:3000/health || echo "未运行"
  ```

### 2. 访问方式

- **本地访问**: `http://localhost:3000`
- **远程访问**: 配置反向代理

### 3. 监控功能

- 检查 Dashboard 运行状态
- 查看访问日志
- 监控资源使用

## 📋 使用示例

### 启动 Dashboard

```
用户：启动 Dashboard
助手：正在启动 OpenClaw-bot-review Dashboard...
      ✅ 启动完成！
      🌐 访问地址：http://localhost:3000
```

### 检查状态

```
用户：Dashboard 运行正常吗？
助手：正在检查...
      ✅ Dashboard 运行中
      📊 端口：3000
      ⏱️ 运行时间：2 小时 15 分
```

## 🔧 配置

```bash
# Dashboard 端口
PORT=3000

# OpenClaw Gateway 地址
OPENCLAW_GATEWAY_URL=http://localhost:18789
```

## 🚀 快速开始

### 1. 安装

```bash
cd /root/.copaw
git clone https://github.com/xmanrui/OpenClaw-bot-review.git
cd OpenClaw-bot-review
npm install
```

### 2. 启动

```bash
npm run dev
```

### 3. 访问

打开浏览器：`http://localhost:3000`

---

**版本：** 1.0  
**创建时间：** 2026-03-22  
**适配目标：** OpenClaw-bot-review → CoPaw
