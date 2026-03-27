#!/bin/bash
# CoPaw 心跳检查脚本
# 执行 HEARTBEAT.md 中定义的每日三问

DATE=$(date +%Y-%m-%d)
LOG_FILE="/root/.copaw/logs/heartbeat_${DATE}.log"

echo "=== CoPaw Heartbeat $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 1. 检查今日记忆文件
MEMORY_FILE="/root/.copaw/memory/${DATE}.md"
if [ ! -f "$MEMORY_FILE" ]; then
    mkdir -p /root/.copaw/memory
    echo "# ${DATE} 记忆文件\n\n> 创建时间：$(date '+%Y-%m-%d %H:%M:%S') CST\n> 心跳触发自动创建\n\n---\n\n## 事件记录\n\n（暂无事件）" > "$MEMORY_FILE"
    echo "[✓] 创建今日记忆文件: $MEMORY_FILE" >> "$LOG_FILE"
else
    echo "[✓] 今日记忆文件已存在: $MEMORY_FILE" >> "$LOG_FILE"
fi

# 2. 检查日志目录最新文件
LATEST_LOG=$(ls -t /root/.copaw/logs/*.log 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    LATEST_TIME=$(stat -c %y "$LATEST_LOG" 2>/dev/null | cut -d'.' -f1)
    echo "[i] 最新日志: $LATEST_LOG ($LATEST_TIME)" >> "$LOG_FILE"
else
    echo "[i] logs/ 目录无 .log 文件" >> "$LOG_FILE"
fi

# 3. 检查 tests 目录（如果存在）
if [ -d "/root/.copaw/tests" ]; then
    LATEST_TEST=$(ls -t /root/.copaw/tests/*.json 2>/dev/null | head -1)
    if [ -n "$LATEST_TEST" ]; then
        TEST_TIME=$(stat -c %y "$LATEST_TEST" 2>/dev/null | cut -d'.' -f1)
        echo "[i] 最新测试: $LATEST_TEST ($TEST_TIME)" >> "$LOG_FILE"
    fi
fi

echo "[✓] 心跳检查完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"