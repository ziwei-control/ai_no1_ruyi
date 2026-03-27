#!/bin/bash
# ========================================
# Eat Service Guardian Script
# 检查 80 端口是否由 eat 的 node 进程占用
# 异常时自动重启 + 发送告警邮件
# ========================================

# 配置
LOG_FILE="/root/.copaw/logs/eat_guard.log"
EMAIL_TO="pandac00@163.com"
FAILED_THRESHOLD=3  # 连续失败次数
NODE_PID_FILE="/var/run/eat_node.pid"
ALERT_LOG="/root/.copaw/logs/eat_alert.log"

# 创建日志目录
mkdir -p /root/.copaw/logs
mkdir -p /var/run

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 eat 服务是否存活（端口 + 进程双验证）
check_eat_service() {
    # 检查端口 80 是否被 node 进程占用（排除 copaw 的 8088）
    local port_check=$(ss -tulnp 2>/dev/null | grep ':80.*users:(("node"' || true)
    
    # 检查 node app.js 进程
    local process_check=$(ps aux | grep "node.*app.js" | grep -v grep | grep -v "guardian.sh" | head -1 || true)
    
    # 提取 PID（优先从进程列表提取，因为 ss 输出复杂）
    local pid=""
    
    if [ -n "$process_check" ]; then
        pid=$(echo "$process_check" | awk '{print $2}')
    elif [ -n "$port_check" ]; then
        # fallback: 从 ss 输出提取（格式：users:(("node",pid=12345,fd=21))）
        pid=$(echo "$port_check" | grep -oP 'pid=\K[0-9]+' | head -1)
    fi
    
    if [ -n "$pid" ]; then
        echo "$pid"
        return 0  # 成功
    else
        return 1  # 失败
    fi
}

# 发送告警邮件
send_alert_email() {
    local subject="⚠️ Eat 服务告警 - $(date '+%Y-%m-%d %H:%M:%S')"
    local body="Eat 服务已失败 $FAILED_THRESHOLD 次！\n\n时间: $(date)\n状态: 端口 80 无 node 服务\n自动重启: 已尝试\n\n请立即检查！\n\n系统信息:\n$(uname -a)\n currentNodePID: $1\n\n日志:\n$(tail -20 $LOG_FILE 2>/dev/null || echo 'No log found')\n\n管理员: pandac00@163.com"
    
    echo "$body" | mail -s "$subject" "$EMAIL_TO" 2>/dev/null || {
        log "[ALERT EMAIL] 发送失败（检查 mail 命令是否安装）"
    }
}

# 自动重启 eat 服务
restart_eat_service() {
    log "[RESTART] 正在重启eat服务..."
    
    # 停止可能残留的进程
    pkill -9 -f "node.*app.js" 2>/dev/null || true
    sleep 2
    
    # 启动 eat 服务（使用 `/root/eat/app.js`）
    cd /root/eat || { log "[ERROR] cd /root/eat 失败"; return 1; }
    
    # 检查 pm2 是否存在
    if command -v pm2 &> /dev/null; then
        pm2 start /root/eat/app.js --name "chileme-app" --no-daemon > /dev/null 2>&1 || {
            pm2 start /root/eat/app.js --name "chileme-app" > /dev/null 2>&1
        }
        log "[PM2] 启动成功"
    else
        # fallback: 直接 node 启动（无守护）
        nohup node /root/eat/app.js > /root/.copaw/logs/eat.log 2>&1 &
        log "[NODE] 直接启动成功，PID: $!"
    fi
    
    sleep 3
    
    # 验证重启是否成功
    local final_check=$(check_eat_service)
    if [ $? -eq 0 ]; then
        log "[SUCCESS] 重启成功，node PID: $final_check"
        return 0
    else
        log "[FAILED] 重启失败，请手动检查"
        return 1
    fi
}

# 主循环
main() {
    log "========================================"
    log "[START] Eat Guardian 启动（每30分钟检查一次）"
    log "========================================"
    
    local failed_count=0
    local last_alert_time=0
    
    while true; do
        log "[CHECK] 正在检查eat服务状态..."
        
        # 检查服务
        local current_pid=$(check_eat_service)
        
        if [ $? -eq 0 ]; then
            # 成功
            log "[OK] Eat 服务正常运行（PID: $current_pid）"
            
            # 更新 PID 文件
            echo "$current_pid" > "$NODE_PID_FILE" 2>/dev/null || true
            failed_count=0
            
        else
            # 失败
            log "[ERROR] Eat 服务异常（端口 80 无 node 服务）"
            failed_count=$((failed_count + 1))
            
            # 记录到 alert log
            echo "[$(date '+%Y-%m-%d %H:%M:%S')]FAILED - failed_count=$failed_count" >> "$ALERT_LOG"
            
            # 连续失败 ≥ 阈值 → 尝试重启
            if [ $failed_count -ge $FAILED_THRESHOLD ]; then
                log "[CRITICAL] 连续失败 $failed_count 次，尝试自动重启..."
                
                if restart_eat_service; then
                    failed_count=0
                    log "[SUCCESS] 自动重启成功"
                    
                    # 发送恢复邮件（避免频繁告警，间隔 ≥ 2 小时）
                    local now=$(date +%s)
                    if [ $((now - last_alert_time)) -gt 7200 ]; then
                        send_alert_email "$current_pid"
                        last_alert_time=$now
                    fi
                    
                else
                    log "[ALERT] 严重故障！请立即检查！"
                    
                    # 告警邮件（减少频率）
                    local now=$(date +%s)
                    if [ $((now - last_alert_time)) -gt 7200 ]; then
                        send_alert_email "$current_pid"
                        last_alert_time=$now
                    fi
                fi
            fi
        fi
        
        # 休眠 30 秒（原 30 分钟 = 1800 秒）
        log "[WAIT] 等待 30 秒，下次检查..."
        sleep 30
    done
}

# 执行主循环
main
