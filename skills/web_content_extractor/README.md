# Web Content Extractor Skill

## 🎯 技能概述

**网页内容提取器** - 智能提取网页正文内容，支持多种提取策略和自动 fallback 机制。

## 📁 文件结构

```
web_content_extractor/
├── README.md           # 本文件 - 快速开始指南
├── SKILL.md            # 完整技能文档
├── extract.sh          # 可执行提取脚本
└── EXAMPLES.md         # 使用示例
```

## 🚀 快速开始

### 方法 1: 在对话中使用

直接提供 URL 给助手：

```
用户：帮我读取这篇文章
https://example.com/article

助手：🔄 正在提取网页内容...
[自动执行提取流程]
```

### 方法 2: 使用命令行脚本

```bash
cd /root/.copaw/skills/web_content_extractor

# 提取单个 URL
./extract.sh "https://example.com/article"

# 带关键词（用于 GitHub 搜索补充）
./extract.sh "https://mp.weixin.qq.com/s/xxx" "OpenClaw Dashboard"
```

## ✨ 核心特性

1. **多策略提取** - 自动尝试多种方法
   - r.jina.ai API（优先）
   - curl 移动端模拟
   - GitHub 搜索补充
   - 缓存服务备用

2. **智能 Fallback** - 无缝切换提取方法
   - 自动检测失败
   - 记录尝试历史
   - 最优结果整合

3. **内容固化** - 自动保存到本地
   - Markdown 格式
   - 包含元数据
   - 结构化存档

4. **特殊支持** - 针对困难网站优化
   - 微信公众号
   - 知乎
   - 技术博客
   - GitHub 项目

## 📊 使用示例

### 示例 1: 普通网页

```bash
./extract.sh "https://example.com"
```

输出：
```
📄 存档位置：/root/.copaw/memory/web_archive_example_com_20260322_202114.md
📊 提取方法：r.jina.ai API
📋 状态：✅ 成功
```

### 示例 2: 微信公众号（困难）

```bash
./extract.sh "https://mp.weixin.qq.com/s/fr9vs8pEc8wRGcwKhtMgOw" "OpenClaw Dashboard"
```

输出：
```
📄 存档位置：/root/.copaw/memory/web_archive_mp_weixin_qq_com_20260322_202130.md
📊 提取方法：curl + GitHub 搜索
📋 状态：⚠️ 部分成功
```

### 示例 3: GitHub 项目

```bash
./extract.sh "https://github.com/openclaw/openclaw"
```

输出：
```
📄 存档位置：/root/.copaw/memory/web_archive_github_com_openclaw_20260322_202200.md
📊 提取方法：r.jina.ai API
📋 状态：✅ 成功
```

## 📁 输出文件

生成的档案包含：

```markdown
# 网页内容存档

## 元数据
- **URL：** https://...
- **提取时间：** 2026-03-22 20:21:14
- **提取方法：** r.jina.ai API
- **状态：** ✅ 成功

---

## 正文内容

[提取的文章内容]

---

## 技术信息
- 生成时间：...
- 存档位置：...
```

## 🔧 配置选项

编辑 `extract.sh` 修改配置：

```bash
# 超时设置（秒）
TIMEOUT_SHORT=30
TIMEOUT_LONG=60
TIMEOUT_XLONG=90

# 存档目录
MEMORY_DIR="/root/.copaw/memory"
```

## 📚 完整文档

- **SKILL.md** - 详细技术文档和使用说明
- **EXAMPLES.md** - 更多使用示例和最佳实践
- **extract.sh** - 实际执行的脚本

## 🎓 学习资源

- [r.jina.ai 文档](https://r.jina.ai/)
- [curl 官方文档](https://curl.se/docs/)

## ⚠️ 使用限制

- ✅ 仅用于个人学习和研究
- ✅ 尊重网站 robots.txt
- ✅ 控制请求频率
- ❌ 不用于商业用途
- ❌ 不提取敏感信息

## 📞 故障排除

**Q: 提取失败怎么办？**
A: 检查网络连接，稍后重试，或手动复制内容

**Q: 中文乱码？**
A: 网站可能使用不同编码，建议手动访问

**Q: 所有方法都失败？**
A: 网站可能有强反爬虫，建议用户提供截图

## 🎯 最佳实践

1. **优先使用 r.jina.ai** - 最快最干净
2. **提供关键词** - 帮助 GitHub 搜索补充
3. **检查存档** - 确认内容完整性
4. **手动补充** - 必要时手动复制原文

---

**创建时间：** 2026-03-22
**版本：** 1.0
**维护者：** 如意 (Ruyi)
