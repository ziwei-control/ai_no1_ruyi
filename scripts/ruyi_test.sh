#!/usr/bin/env bash
#如意测试脚本 - 测试 echo 和其他命令
set -e

echo "🚀 开始如意测试..."

echo "测试1: echo 命令"
echo "test1"

echo "测试2: ls 命令"
ls -la /root/.copaw/scripts/

echo "测试3: 当前时间"
date

echo "✅ 所有测试通过！"
