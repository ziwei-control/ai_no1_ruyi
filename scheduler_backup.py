#!/usr/bin/env python3
"""
如意 Scheduler（高级调度器）
- 任务依赖图解析与调度
- 并发控制（支持多任务并发执行）
- 熔断机制（连续失败达到阈值后跳过）
- 资源配额（时间/内存）
- 优先级队列（高/正常/低）
- Plugin链执行
"""

import os
import sys
import json
import time
import subprocess
import resource
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class Priority(Enum):
    HIGH = 1
    NORMAL = 2
    LOW = 3


class CircuitState(Enum):
    CLOSED = 1       # 正常
    OPEN = 2         # 熔断（失败过多）
    HALF_OPEN = 3    # 半开（尝试恢复）


class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    CIRCUIT_BROKEN = "熔断"
    TIMEOUT = "timeout"


@dataclass
class Task:
    name: str
    target: str
    priority: Priority = Priority.NORMAL
    dependencies: List[str] = field(default_factory=list)
    max_failures: int = 3
    timeout: int = 120
    max_retries: int = 1
    memory_limit: int = 512  # MB
    status: ExecutionStatus = ExecutionStatus.PENDING
    failure_count: int = 0
    results: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)  # 新增 metadata 字段


@dataclass
class ExecutionResult:
    task: str
    status: ExecutionStatus
    exit_code: int
    timestamp: datetime
    duration: float
    output: str = ""
    error: str = ""
    metadata: Dict = field(default_factory=dict)


class RuyiScheduler:
    def __init__(self, working_dir: str = "/root/.copaw", controller=None):
        self.working_dir = working_dir
        self.controller = controller
        self.tasks: List[Task] = []
        self.results: List[ExecutionResult] = []
        self.circuit_states: Dict[str, CircuitState] = {}
        self.max_concurrent = 1
        self.start_time = None
        self.plugins = {}
        
    def register_plugin(self, name: str, handler: Callable):
        """注册插件处理器"""
        self.plugins[name] = handler
        print(f"✅ 插件注册: {name}")
        
    def load_dependencies(self, deps_file: str) -> bool:
        """加载任务依赖图"""
        deps_path = Path(deps_file)
        if not deps_path.exists():
            print(f"❌ 依赖文件不存在: {deps_file}")
            return False
            
        try:
            with open(deps_path, 'r', encoding='utf-8') as f:
                deps = json.load(f)
                
            for task_name, task_config in deps.items():
                task = Task(
                    name=task_name,
                    target=task_config.get('target', ''),
                    priority=Priority[task_config.get('priority', 'NORMAL').upper()],
                    dependencies=task_config.get('dependencies', []),
                    max_failures=task_config.get('failures_threshold', 3),
                    timeout=task_config.get('timeout', 120),
                    max_retries=task_config.get('retries', 1),
                    memory_limit=task_config.get('memory_limit', 512)
                )
                self.tasks.append(task)
                
            print(f"✅ 加载依赖图: {len(self.tasks)} 个任务")
            return True
        except Exception as e:
            print(f"❌ 加载依赖图失败: {e}")
            return False
    
    def create_main_task(self, parsed: Dict) -> Task:
        """从解析输入创建主任务"""
        target = parsed.get('target', 'unknown')
        params = parsed.get('params', {})
        
        # 移除路径中的特殊字符，作为任务名
        name = target.replace('/', '_').replace('.', '_').replace(' ', '_').strip('_')
        if not name:
            name = 'main_task'
            
        task = Task(
            name=name[:50],  # 限制长度
            target=target,
            priority=Priority[
                params.get('--priority', 'NORMAL').upper()
                if params.get('--priority') in ['HIGH', 'NORMAL', 'LOW']
                else 'NORMAL'
            ],
            max_failures=params.get('--failures-threshold', 3),
            timeout=params.get('--timeout', 120),
            max_retries=params.get('--counts', 1),
            memory_limit=512
        )
        
        return task
    
    def get_pending_tasks(self, completed: List[str]) -> List[Task]:
        """获取等待执行的任务（无待定依赖）"""
        pending = []
        for task in self.tasks:
            if task.status == ExecutionStatus.PENDING:
                # 检查依赖是否都已完成
                if not task.dependencies or all(
                    any(t.name == d and t.status == ExecutionStatus.SUCCESS for t in self.tasks)
                    for d in task.dependencies
                ):
                    pending.append(task)
        
        # 按优先级排序
        pending.sort(key=lambda t: t.priority.value)
        return pending
    
    def check_circuit(self, task: Task) -> bool:
        """检查熔断器状态"""
        if task.name not in self.circuit_states:
            self.circuit_states[task.name] = CircuitState.CLOSED
            
        state = self.circuit_states[task.name]
        if state == CircuitState.OPEN:
            task.status = ExecutionStatus.CIRCUIT_BROKEN
            return False
        return True
    
    def record_success(self, task: Task):
        """记录成功"""
        self.circuit_states[task.name] = CircuitState.CLOSED
        task.failure_count = 0
        print(f"✅ 任务成功: {task.name}")
        
    def record_failure(self, task: Task) -> bool:
        """记录失败，检查是否触发熔断
        返回: True = 应该熔断, False = 继续
        """
        task.failure_count += 1
        print(f"❌ 任务失败: {task.name} (失败计数: {task.failure_count}/{task.max_failures})")
        
        if task.failure_count >= task.max_failures:
            self.circuit_states[task.name] = CircuitState.OPEN
            task.status = ExecutionStatus.CIRCUIT_BROKEN
            print(f"🔴 熔断触发: {task.name} (连续失败 {task.failure_count} 次)")
            return True
        return False
    
    def execute_command(self, command: str, timeout: int = 60, verbose: bool = False) -> ExecutionResult:
        """执行命令并返回结果"""
        start_time = time.time()
        
        try:
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                duration = time.time() - start_time
                exit_code = proc.returncode
                
                result = ExecutionResult(
                    task=command[:50] if len(command) > 50 else command,
                    status=ExecutionStatus.SUCCESS if exit_code == 0 else ExecutionStatus.FAILURE,
                    exit_code=exit_code,
                    timestamp=datetime.now(),
                    duration=duration,
                    output=stdout,
                    error=stderr
                )
                
                if verbose and stdout:
                    print(f"\t输出: {stdout.strip()}")
                if verbose and stderr and exit_code != 0:
                    print(f"\t错误: {stderr.strip()}")
                    
                return result
                
            except subprocess.TimeoutExpired:
                proc.kill()
                duration = time.time() - start_time
                return ExecutionResult(
                    task=command[:50],
                    status=ExecutionStatus.TIMEOUT,
                    exit_code=-1,
                    timestamp=datetime.now(),
                    duration=duration,
                    error=f"命令执行超时 ({timeout}s)"
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return ExecutionResult(
                task=command[:50],
                status=ExecutionStatus.FAILURE,
                exit_code=-1,
                timestamp=datetime.now(),
                duration=duration,
                error=str(e)
            )
    
    def execute_task(self, task: Task, verbose: bool = False) -> ExecutionResult:
        """执行单个任务"""
        print(f"\n🚀 开始任务: {task.name}")
        print(f"   目标: {task.target}")
        print(f"   超时: {task.timeout}s | 重试: {task.max_retries}")
        
        # 检查熔断
        if not self.check_circuit(task):
            result = ExecutionResult(
                task=task.name,
                status=ExecutionStatus.CIRCUIT_BROKEN,
                exit_code=-1,
                timestamp=datetime.now(),
                duration=0
            )
            self.results.append(result)
            return result
        
        # 执行主逻辑
        result = None
        
        for attempt in range(task.max_retries):
            print(f"\t重试 {attempt + 1}/{task.max_retries}")
            
            # 执行命令
            result = self.execute_command(
                task.target,
                timeout=task.timeout,
                verbose=verbose
            )
            
            if result.status == ExecutionStatus.SUCCESS:
                print(f"\t✅ 成功 (耗时 {result.duration:.2f}s)")
                break
            elif result.status == ExecutionStatus.TIMEOUT:
                print(f"\t⏱️ 超时")
            else:
                print(f"\t❌ 失败 (退出码: {result.exit_code})")
            
            # 记录失败
            if attempt < task.max_retries - 1:
                self.record_failure(task)
                if self.circuit_states.get(task.name) == CircuitState.OPEN:
                    break
        
        # 检查最终结果
        if result and result.status == ExecutionStatus.SUCCESS:
            self.record_success(task)
            task.status = ExecutionStatus.SUCCESS
        elif result:
            task.status = ExecutionStatus.FAILURE
        
        self.results.append(result)
        return result
    
    def run_plugin(self, plugin_name: str, context: Dict) -> Dict:
        """运行指定插件"""
        handler = self.plugins.get(plugin_name)
        if not handler:
            print(f"⚠️ 插件未注册: {plugin_name}")
            return context
            
        print(f"🔧 运行插件: {plugin_name}")
        try:
            result = handler(context)
            if result:
                context.update(result)
            return context
        except Exception as e:
            print(f"❌ 插件执行失败: {plugin_name}: {e}")
            context['plugin_error'] = f"{plugin_name}: {e}"
            return context
    
    def run_plugin_chain(self, parsed: Dict) -> Dict:
        """运行插件链"""
        print("\n🧪 如意 Scheduler 启动...")
        
        # Step 1: 注册标准插件
        self.register_plugin('nlp', self._nlp_plugin)
        self.register_plugin('path', self._path_plugin)
        self.register_plugin('exec', self._exec_plugin)
        self.register_plugin('report', self._report_plugin)
        self.register_plugin('evolve', self._evolve_plugin)
        
        # Step 2: 创建主任务
        task = self.create_main_task(parsed)
        self.tasks = [task]
        
        # Step 3: 加载依赖（如果有）
        params = parsed.get('params', {})
        if '--dependencies' in params:
            self.load_dependencies(params['--dependencies'])
        
        # Step 4: 获取并发设置
        self.max_concurrent = params.get('--concurrent', 1)
        verbose = params.get('--verbose', False)
        
        # Step 5: 运行插件链
        context = {
            'parsed': parsed,
            'task': task,
            'controller': self.controller,
            'results': [],
            'errors': []
        }
        
        # 依次运行插件
        plugins_order = ['nlp', 'path', 'exec', 'report', 'evolve']
        for plugin_name in plugins_order:
            context = self.run_plugin(plugin_name, context)
            if 'error' in context:
                break
        
        # Step 6: 检查最终状态
        status = 'success'
        if context.get('error'):
            status = 'error'
        else:
            # 检查执行结果
            for r in self.results:
                if r.status not in [ExecutionStatus.SUCCESS, ExecutionStatus.CIRCUIT_BROKEN]:
                    status = 'failure'
                    break
        
        return {
            'status': status,
            'results': self.results,
            'report': context.get('report', ''),
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
    
    # 标准插件实现
    def _nlp_plugin(self, context: Dict) -> Dict:
        """NLP 插件: 解析输入，提取参数"""
        parsed = context['parsed']
        
        print(f"🔍 NLP 插件: 解析输入")
        print(f"   意图: {parsed['command']}")
        print(f"   目标: {parsed['target']}")
        print(f"   参数: 次数={parsed['params'].get('--counts')}, 超时={parsed['params'].get('--timeout')}")
        
        # 确保任务有正确的参数
        task = context['task']
        task.timeout = parsed['params'].get('--timeout', 60)
        task.max_retries = parsed['params'].get('--counts', 1)
        task.max_failures = parsed['params'].get('--failures-threshold', 3)
        
        return context
    
    def _path_plugin(self, context: Dict) -> Dict:
        """Path 插件: 验证路径，提取脚本类型"""
        task = context['task']
        target = task.target
        
        print(f"📂 Path 插件: 验证路径")
        print(f"   原始目标: {target}")
        
        # 检查目标
        if not target:
            context['error'] = "目标为空"
            return context
        
        # 从目标中提取可执行部分
        # 如果 target 是完整句子，尝试提取命令部分
        import re
        # 匹配路径或命令（以 / 开头，或以常见扩展名结尾）
        cmd_match = re.search(r'^(/[\w/._-]+(?:\.\w+)?)', target)
        if cmd_match:
            target = cmd_match.group(1)
            task.target = target
        elif ' ' in target and not target.startswith('/'):
            # 检查是否是 docker/curl/wget 命令
            if target.startswith('docker run'):
                pass  # 保持原样
            elif target.startswith('curl ') or target.startswith('wget '):
                pass  # 保持原样
            else:
                # 尝试提取第一个参数
                parts = target.split()
                if len(parts) > 0:
                    target = parts[0]
                    task.target = target
        
        print(f"   提取目标: {target}")
        
        # 检查本地文件
        if target.startswith('/') or target.startswith('./') or target.startswith('../'):
            path = Path(target)
            if not path.exists():
                context['error'] = f"目标不存在: {target}"
                return context
            
            task.target = f"{'.' if target.startswith('./') else ''}{target}"  # 保持相对路径
            
            # 判断脚本类型
            if target.endswith('.py'):
                task.metadata['script_type'] = 'Python'
            elif target.endswith('.sh'):
                task.metadata['script_type'] = 'Bash'
            elif target.endswith('.pl'):
                task.metadata['script_type'] = 'Perl'
            elif target.endswith('.rb'):
                task.metadata['script_type'] = 'Ruby'
            else:
                # 检查 shebang
                try:
                    with open(path, 'r') as f:
                        first_line = f.readline()
                        if first_line.startswith('#!'):
                            task.metadata['shebang'] = first_line.strip()
                            if 'python' in first_line:
                                task.metadata['script_type'] = 'Python'
                            elif 'bash' in first_line or 'sh' in first_line:
                                task.metadata['script_type'] = 'Bash'
                except:
                    pass
        
        # 检查是否为命令
        elif ' ' not in target:
            import shutil
            if shutil.which(target):
                task.metadata['command_type'] = 'system'
            else:
                context['error'] = f"命令不存在: {target}"
                return context
        
        # Docker 命令
        elif target.startswith('docker run'):
            task.metadata['script_type'] = 'Docker'
        
        # 网络命令
        elif target.startswith('curl ') or target.startswith('wget '):
            task.metadata['script_type'] = 'Network'
        
        else:
            task.metadata['script_type'] = 'Unknown'
        
        print(f"   类型: {task.metadata.get('script_type', 'Unknown')}")
        print(f"   ✅ 路径验证通过")
        
        return context
    
    def _exec_plugin(self, context: Dict) -> Dict:
        """Exec 插件: 执行任务"""
        task = context['task']
        verbose = context['parsed']['params'].get('--verbose', False)
        
        print(f"⚙️  Exec 插件: 执行任务")
        
        try:
            result = self.execute_task(task, verbose=verbose)
            context['results'].append(result)
            
            if result.status == ExecutionStatus.SUCCESS:
                print(f"   ✅ 执行成功")
            else:
                print(f"   ❌ 执行失败: {result.status.value}")
                context['error'] = f"任务执行失败: {result.status.value}"
                
        except Exception as e:
            context['error'] = str(e)
            print(f"   ❌ 执行异常: {e}")
        
        return context
    
    def _report_plugin(self, context: Dict) -> Dict:
        """Report 插件: 生成报告"""
        print(f"📝 Report 插件: 生成报告")
        
        lines = [
            "# 📋 测试报告如意（Ruyi）",
            "",
            f"- **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **调度器**: RuyiScheduler",
            "",
            "## 🧪 多轮时间线",
            "",
            "| 任务 | 状态 | 退出码 | 耗时 |",
            "|------|------|--------|------|",
        ]
        
        success_count = 0
        failure_count = 0
        circuit_broken_count = 0
        
        for r in self.results:
            lines.append(f"| {r.task} | {r.status.value} | {r.exit_code} | {r.duration:.2f}s |")
            
            if r.status == ExecutionStatus.SUCCESS:
                success_count += 1
            elif r.status == ExecutionStatus.CIRCUIT_BROKEN:
                circuit_broken_count += 1
            else:
                failure_count += 1
        
        lines.extend([
            "",
            "## 📊 统计", 
            "",
            f"- **总任务数**: {len(self.results)}",
            f"- **成功**: {success_count}",
            f"- **失败**: {failure_count}",
            f"- **熔断**: {circuit_broken_count}",
            "",
            "## 🔄 熔断状态",
            "",
        ])
        
        if self.circuit_states:
            for task, state in self.circuit_states.items():
                lines.append(f"- {task}: {state.name}")
        else:
            lines.append("- 无熔断")
        
        lines.extend([
            "",
            "*报告由如意 Scheduler 生成*",
        ])
        
        report = '\n'.join(lines)
        context['report'] = report
        
        # 确定最终状态
        if circuit_broken_count > 0 and failure_count == 0:
            context['status'] = 'success'
        elif failure_count > 0:
            context['status'] = 'failure'
        else:
            context['status'] = 'success'
        
        print(f"   ✅ 报告生成完成")
        print(f"   详情: {success_count} 成功, {failure_count} 失败, {circuit_broken_count} 熔断")
        
        return context
    
    def _evolve_plugin(self, context: Dict) -> Dict:
        """Evolve 插件: 自动化进化"""
        print(f"🔄 Evolve 插件: 进化分析")
        
        # 检查是否需要生成修复版
        has_failure = any(
            r.status not in [ExecutionStatus.SUCCESS, ExecutionStatus.CIRCUIT_BROKEN]
            for r in self.results
        )
        
        if has_failure:
            print(f"   ⚠️  检测到失败，建议生成修复版")
            
            # 生成修复建议
            context['evolve_suggestion'] = {
                'action': 'generate_fix_skill',
                'based_on': 'ai_no1_fix/v2/',
                'reason': '任务执行失败，需要生成修复版 Skill'
            }
            
        else:
            print(f"   ✅ 全部成功，无需修复")
            context['evolve_suggestion'] = {
                'action': 'skip',
                'reason': '任务全部成功'
            }
        
        return context
    
    def run_with_concurrency(self, verbose: bool = False) -> List[ExecutionResult]:
        """并发执行所有任务"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = {}
            pending = self.get_pending_tasks([])
            
            while pending or futures:
                # 启动新任务
                for task in pending[:self.max_concurrent - len(futures)]:
                    future = executor.submit(self.execute_task, task, verbose)
                    futures[future] = task
                
                # 检查完成的任务
                for future in as_completed(futures):
                    task = futures.pop(future)
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        print(f"❌ 任务 {task.name} 异常: {e}")
                        results.append(ExecutionResult(
                            task=task.name,
                            status=ExecutionStatus.FAILURE,
                            exit_code=-1,
                            timestamp=datetime.now(),
                            duration=0,
                            error=str(e)
                        ))
                
                # 更新待处理列表
                completed = [r.task for r in results]
                pending = self.get_pending_tasks(completed)
        
        return results


def main():
    scheduler = RuyiScheduler()
    
    # 测试命令
    test_commands = [
        ("echo hello", 5),
        ("ls -la /root/.copaw", 10),
        ("echo test", 3),
    ]
    
    for cmd, timeout in test_commands:
        result = scheduler.execute_command(cmd, timeout=timeout, verbose=True)
        scheduler.results.append(result)
        print(f"\n结果: {result.status.value}")
    
    # 生成报告
    report = scheduler._report_plugin({'context': {}})['context'].get('report', '')
    print("\n" + report)


if __name__ == '__main__':
    main()
