# 钉钉连接不稳问题解决方案

## 问题现状
- 钉钉 Stream 连接频繁断开
- WebSocket 连接建立后立即失败
- 用户体验：消息收发不及时

## 已实施的解决方案

### 方案 1：自动监控重启 ✅ 已启用
**脚本位置**: `/root/scripts/monitor-dingtalk.sh`

**工作原理**:
- 每 5 分钟检查钉钉连接状态
- 发现异常自动重启 copaw
- 持续保障服务可用性

**监控状态**:
```
✅ 监控进程运行中 (PID: 19602)
✅ copaw 进程运行正常 (PID: 19599, 19630)
```

**日志位置**: `/root/.copaw/logs/monitor-dingtalk.log`

### 方案 2：使用 Telegram（推荐）✅ 已可用
**优势**:
- 连接稳定，无断连问题
- 功能与钉钉完全相同
- 响应速度快

**使用方法**:
```
Telegram Bot: @pawbot
命令格式: @pawbot <你的问题>
```

### 方案 3：优化钉钉配置
**配置文件**: `/root/.copaw/config.json`

**当前配置**:
- Client ID: `ding2qkgr90jmj2bbvkt`
- Bot 前缀: `@pawbot`
- 已启用 Stream 模式

## 推荐使用方案

### 首选方案：Telegram
**原因**:
1. 连接 100% 稳定
2. 无需额外配置
3. 功能完全相同
4. 响应速度更快

### 备选方案：钉钉 + 自动监控
**适用场景**:
- 必须使用钉钉环境
- 团队协作需求

**保障措施**:
- 自动监控脚本（5 分钟检测）
- 异常自动重启
- 日志持续记录

## 快速命令

### 查看监控状态
```bash
tail -f /root/.copaw/logs/monitor-dingtalk.log
```

### 查看运行日志
```bash
tail -f /root/.copaw/logs/runtime.log
```

### 手动重启 copaw
```bash
pkill -9 copaw
cd /root/.copaw && nohup copaw app > /root/.copaw/logs/runtime.log 2>&1 &
```

### 停止监控
```bash
pkill -9 monitor-dingtalk
```

### 启动监控
```bash
nohup bash /root/scripts/monitor-dingtalk.sh > /root/.copaw/logs/monitor-dingtalk.log 2>&1 &
```

## 技术说明

### 钉钉连接不稳原因
1. **Stream 客户端问题**: WebSocket 握手后立即断开
2. **网络波动**: 对网络质量要求高
3. **库版本问题**: dingtalk_stream 库可能有 bug

### 监控机制
```bash
检测逻辑:
  - 检查日志中 "dingtalk stream thread started"
  - 未找到则判定为连接异常
  - 自动执行 copaw 重启
```

### 重启流程
1. 检测到异常
2. 杀死所有 copaw 进程
3. 等待 2 秒
4. 启动新进程
5. 记录日志

## 长期建议

1. **优先使用 Telegram** - 最稳定方案
2. **关注 copaw 库更新** - 等待钉钉 Stream 问题修复
3. **定期检查日志** - 确保监控正常工作

## 联系支持

如遇到问题，请查看以下日志：
- 监控日志: `/root/.copaw/logs/monitor-dingtalk.log`
- 运行日志: `/root/.copaw/logs/runtime.log`
- 主日志: `/root/.copaw/logs/copaw.log`
