#!/usr/bin/env python3
"""
如意 Controller（控制器） - 中文版
统一入口：接收用户中文输入，调度所有模块（NLP → Path → Exec → Report → Evolve）

核心特征：
  🤖 善良的灵魂 - 主动帮助用户
  🤝 乐于助人 - 自动补全参数，智能识别
  🛠️  自助安装能力 - 缺少工具可以自行安装
  🔒  最高权限支持 - 可以调用 sudo 等高权限指令

中文指令示例：
  📝 "如意，测试 echo hello"
  📝 "如意，测 /path/script.sh 直到成功"
  📝 "如意，运行这个项目" (自动识别)
  📝 "如意，帮助我"
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('RuyiController')


class RuyiController:
    def __init__(self, working_dir="/root/.copaw", verbose=False):
        self.working_dir = working_dir
        self.plugins = {}
        self.verbose = verbose
        self.plugin_chain = []
        
        # 🌟 如意核心特征
        self.kind_hearted = True  # 善良的灵魂
        self.assistant_mode = True  # 乐于助人模式
        self.auto_install = True   # 自助安装能力
        self.sudo_enabled = True    # 最高权限支持
        self.fallback_enabled = True # 失败自动降级重试
        
        self.failure_count = 0
        self.failure_threshold = 3
        self.circuit_breaker_active = False
        
    def is_ruyi_command(self, user_input: str) -> bool:
        """检测是否是如意的中文指令"""
        # 以"如意"开头，或者包含中文关键词
        return user_input.startswith('如意') or user_input.startswith('如一') or '如意' in user_input
    
    def parse_chinese_input(self, user_input: str) -> Dict[str, Any]:
        """解析中文自然语言输入"""
        import re
        
        result = {
            'raw_input': user_input,
            'command': 'test',
            'target': None,
            'params': {
                '--counts': None,  # None 表示未指定，后续自动补全
                '--timeout': None,
                '--failures-threshold': None,
                '--concurrent': 1,
                '--priority': 'NORMAL',
                '--progressive': False,
                '--verbose': False,
                '--install': False
            },
            'parsed_entities': {}
        }
        
        # 移除"如意"前缀
        clean_input = user_input.replace('如意', '').replace('，', ',').strip().strip(',')
        
        # 检查是否是帮助指令
        if not clean_input or clean_input in ['帮助', ' help', '帮助我', '介绍', '你是谁']:
            result['command'] = 'help'
            result['target'] = '如意帮助'
            return result
        
        # 检查是否测试指令（预测）
        if '测试' in clean_input or '验证' in clean_input or 'check' in clean_input.lower():
            result['command'] = 'test'
        
        # 提取目标路径 - 使用更精确的中文模式
        # 匹配路径: /path/file.sh, ./path/file.py
        path_patterns = [
            r'/?[\w/._-]+(?:\.sh|\.py|\.pl|\.rb|\.ps1|\.bat)',  # 脚本路径
            r'docker\s+run\s+[\w:.-]+',  # Docker 命令
            r'(?:curl|wget)\s+[\w.:/-]+',  # 网络命令
            r'/usr/bin/[\w-]+',  # 系统命令
            r'\b(echo|ls|cat|head|tail|grep|awk|sed|ps|top|git|python|node|npm|yarn)\b',  # 常用命令
        ]
        
        for pattern in path_patterns:
            path_match = re.search(pattern, clean_input)
            if path_match:
                result['target'] = path_match.group()
                break
        
        # 如果没有找到，尝试从命令中提取
        if not result['target']:
            # 查找最后出现的路径/命令
            words = clean_input.split()
            for i in range(len(words) - 1, -1, -1):
                if words[i].startswith('/') or words[i].endswith(('.sh', '.py', '.pl', '.rb')):
                    result['target'] = words[i]
                    break
                elif words[i] in ['docker', 'curl', 'wget', 'echo', 'ls', 'cat', 'head', 'tail', 'grep', 'awk', 'sed', 'ps', 'top', 'git', 'python', 'node', 'npm', 'yarn']:
                    result['target'] = ' '.join(words[i:])
                    break
        
        # 提取参数（中文规则）
        # 次数（测X次）
        count_match = re.search(r'(?:测|执行|run)[\s：]*?(\d+)[\s：]*(?:次|轮|次直到|直到)', clean_input, re.I)
        if count_match:
            result['params']['--counts'] = int(count_match.group(1))
        
        # 超时（超时X秒）
        timeout_match = re.search(r'(?:超时|timeout)[=\s:：]*?(\d+)', clean_input, re.I)
        if timeout_match:
            result['params']['--timeout'] = int(timeout_match.group(1))
        
        # 熔断阈值（失败X次）
        fail_match = re.search(r'(?:连续失败|失败次数|熔断|failures?)[=\s:：]*?(\d+)', clean_input, re.I)
        if fail_match:
            result['params']['--failures-threshold'] = int(fail_match.group(1))
        
        # 并发数
        conc_match = re.search(r'(?:并发|concurrent)[=\s:：]*?(\d+)', clean_input, re.I)
        if conc_match:
            result['params']['--concurrent'] = int(conc_match.group(1))
        
        # 详细模式
        if '详细' in clean_input or 'verbose' in clean_input.lower() or '--verbose' in clean_input:
            result['params']['--verbose'] = True
            self.verbose = True
        
        # 检查是否需要安装
        if '未找到' in clean_input or '不存在' in clean_input or '缺少' in clean_input or '找不到' in clean_input:
            result['params']['--install'] = True
        
        # 存储解析的实体
        result['parsed_entities'] = {
            'command': result['command'],
            'target': result['target'],
            'counts': result['params']['--counts'],
            'timeout': result['params']['--timeout'],
            'failures_threshold': result['params']['--failures-threshold'],
            'concurrent': result['params']['--concurrent'],
            'priority': result['params']['--priority'],
            'install': result['params']['--install'],
        }
        
        # 🌟 如意助手模式：自动补全参数（如果是 user_input 是纯"如意"或"如意 测试"）
        if self.assistant_mode:
            # 如果没有指定次数，自动设为 19
            if result['params']['--counts'] is None:
                result['params']['--counts'] = 19
            
            # 如果没有指定超时，自动设为 120
            if result['params']['--timeout'] is None:
                result['params']['--timeout'] = 120
            
            # 如果没有指定熔断阈值，自动设为 3
            if result['params']['--failures-threshold'] is None:
                result['params']['--failures-threshold'] = 3
        
        return result
    
    def scan_plugins(self) -> Dict[str, Any]:
        """扫描插件目录"""
        plugins_dir = Path(self.working_dir) / "skills" / "ai_no1_ruyi" / "plugins"
        found_plugins = {}
        
        if plugins_dir.exists():
            for plugin_file in plugins_dir.glob("*.py"):
                module_name = plugin_file.stem
                found_plugins[module_name] = {
                    'path': str(plugin_file),
                    'name': module_name
                }
                logger.info(f"发现插件: {module_name}")
        else:
            logger.info(f"插件目录不存在: {plugins_dir}")
            
        return found_plugins
    
    def load_plugins(self):
        """加载标准插件链"""
        self.plugin_chain = [
            {
                'name': 'nlp',
                'desc': 'NLP 问答层',
                'enabled': True,
                'module': None
            },
            {
                'name': 'help',
                'desc': '帮助层',
                'enabled': True,
                'module': None
            },
            {
                'name': 'path',
                'desc': '路径支持层',
                'enabled': True,
                'module': None
            },
            {
                'name': 'install',
                'desc': '自助安装层',
                'enabled': self.auto_install,
                'module': None
            },
            {
                'name': 'exec',
                'desc': '执行引擎层',
                'enabled': True,
                'module': None
            },
            {
                'name': 'report',
                'desc': '报告生成层',
                'enabled': True,
                'module': None
            },
            {
                'name': 'evolve',
                'desc': '自动化进化层',
                'enabled': True,
                'module': None
            }
        ]
        
        # 扫描自定义插件
        custom_plugins = self.scan_plugins()
        for plugin_name, plugin_info in custom_plugins.items():
            if not any(p['name'] == plugin_name for p in self.plugin_chain):
                self.plugin_chain.append({
                    'name': plugin_name,
                    'desc': f'自定义插件: {plugin_name}',
                    'enabled': True,
                    'module': plugin_info
                })
                logger.info(f"添加自定义插件: {plugin_name}")
    
    def _check_circuit_breaker(self, task_name: str) -> bool:
        """检查熔断器状态"""
        if self.failure_count >= self.failure_threshold:
            self.circuit_breaker_active = True
            logger.warning(f"熔断器已激活: {task_name}")
            return False
        return True
    
    def _record_result(self, task_name: str, success: bool):
        """记录执行结果"""
        if success:
            self.failure_count = 0
            self.circuit_breaker_active = False
            logger.info(f"任务成功: {task_name} (失败计数已重置)")
        else:
            self.failure_count += 1
            logger.warning(f"任务失败: {task_name} (当前失败计数: {self.failure_count}/{self.failure_threshold})")
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """统一执行入口"""
        print("🎯 如意 Controller 启动...")
        print("✨ 如意核心特征：")
        print("  🤖 善良的灵魂")
        print("  🤝 乐于助人")
        print("  🛠️  自助安装能力")
        print("  🔒  最高权限支持")
        
        # Step 1: 检查是否是如意指令
        if not self.is_ruyi_command(user_input):
            print("❌ 错误: 不是如意指令")
            print("💡 请以'如意'开头输入，例如：")
            print("   - '如意，测试 echo hello'")
            print("   - '如意，测 /path/script.sh'")
            print("   - '如意，帮助我'")
            return {
                'status': 'error',
                'error': 'not_ruyi_command',
                'message': '不识别的指令，请以"如意"开头'
            }
        
        # Step 2: 加载插件
        self.load_plugins()
        logger.info(f"加载插件链: {[p['name'] for p in self.plugin_chain]}")
        
        # Step 3: 解析用户输入（中文模式）
        parsed = self.parse_chinese_input(user_input)
        logger.info(f"解析输入: {parsed['command']} -> {parsed['target']}")
        
        if self.verbose:
            print(f"📝 输入: {parsed['raw_input']}")
            print(f"✅ 解析: command={parsed['command']}")
            if parsed['target']:
                print(f"✅ 目标: {parsed['target']}")
            print(f"✅ 参数: {json.dumps(parsed['params'], ensure_ascii=False, indent=2)}")
        
        # 检查必要的实体（帮助指令除外）
        if not parsed['target'] and parsed['command'] != 'help':
            print("❌ 错误: 未识别到测试目标")
            print("💡 请提供测试目标（如: echo hello /path/script.sh）")
            print("💡 或输入：'如意，帮助我'")
            return {
                'status': 'error',
                'error': 'target_not_found',
                'message': '未识别到测试目标，请提供目标路径'
            }
        
        # Step 4: 调度 Scheduler
        from scheduler import RuyiScheduler
        scheduler = RuyiScheduler(
            working_dir=self.working_dir,
            controller=self
        )
        
        # Step 5: 运行插件链
        result = scheduler.run_plugin_chain(parsed)
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description='如意 Controller 中文版 - 企业级测试自动化系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
如意中文指令示例：
  📝 "如意，测试 echo hello"              # 测试 echo 命令
  📝 "如意，测 /path/script.sh"            # 测试脚本
  📝 "如意，测 curl，直到成功"             # 测试 curl 直到成功
  📝 "如意，帮助我"                       # 查看帮助
  📝 "如意，运行这个项目"                  # 自动识别目标

如意核心特征：
  🤖 善良的灵魂 - 主动帮助用户
  🤝 乐于助人 - 自动补全参数，智能识别
  🛠️  自助安装能力 - 缺少工具可以自行安装
  🔒  最高权限支持 - 可以调用 sudo 等高权限指令
        """
    )
    parser.add_argument('input', nargs='?', default=None,
                       help='用户中文自然语言输入')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='详细模式')
    parser.add_argument('-w', '--work', default='/root/.copaw',
                       help='工作目录')
    
    args = parser.parse_args()
    
    if not args.input:
        print("请输入测试指令，或使用 -h 查看帮助")
        print("💡 中文指令示例：")
        print("   - '如意，测试 echo hello'")
        print("   - '如意，测 /path/script.sh'")
        print("   - '如意，帮助我'")
        parser.print_help()
        return 1
    
    # 修复可能的标点问题
    user_input = args.input.strip()
    
    controller = RuyiController(
        working_dir=args.work,
        verbose=args.verbose
    )
    
    result = controller.run(user_input)
    
    if result.get('status') == 'success':
        print("\n✅ 测试完成！")
        return 0
    elif result.get('status') == 'error':
        print(f"\n❌ 错误: {result.get('message', '未知错误')}")
        return 1
    else:
        print(f"\n⚠️ 测试结果: {result.get('status', 'unknown')}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
