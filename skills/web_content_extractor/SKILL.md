# Web Content Extractor Skill

## 📖 技能描述

**网页内容提取器** - 智能提取网页正文内容，支持多种提取策略和自动 fallback 机制。

适用于：
- 提取微信公众号文章内容
- 获取新闻/博客文章正文
- 抓取文档和技术文章
- 保存网页内容到本地存档
- 绕过简单的反爬虫机制

## 🎯 使用场景

当用户提到以下关键词时使用此技能：
- "获取网页内容"
- "提取文章"
- "读取链接"
- "保存网页"
- "抓取内容"
- 提供任何 URL 链接并要求读取内容

## 🚀 核心功能

### 1. 多策略提取

按顺序尝试以下方法，直到成功：

1. **r.jina.ai API** - 最简洁的 Markdown 提取
2. **curl 模拟移动端** - 直接获取 HTML
3. **browser_use 浏览器** - 渲染 JavaScript 内容
4. **GitHub/Archive 缓存** - 备用方案

### 2. 智能 Fallback

- 自动检测提取失败（验证码、错误页面）
- 无缝切换到下一种方法
- 记录每种方法的尝试结果

### 3. 内容固化

- 自动保存到 `memory/` 目录
- 生成结构化 Markdown 档案
- 包含元数据（URL、时间、提取状态）

### 4. 特殊网站支持

- **微信公众号**：移动端 UA + 特殊处理
- **知乎**：移动端适配
- **技术博客**：优先提取正文
- **GitHub**：README 和项目信息

## 📋 使用方法

### 基本用法

用户提供 URL 后，自动执行提取流程：

```
用户：帮我读取这篇文章 https://example.com/article
```

技能会自动：
1. 尝试多种方法提取内容
2. 显示提取进度和结果
3. 保存内容到本地档案
4. 返回提取的正文

### 手动调用

在对话中明确提及技能名称：

```
用户：使用 web_content_extractor 读取 https://...
```

## 🔧 技术实现

### 提取方法详解

#### 方法 1: r.jina.ai API

```bash
curl -s --max-time 45 "https://r.jina.ai/http://<URL>"
```

**优点：**
- 返回干净的 Markdown
- 自动去除广告和导航
- 速度快

**缺点：**
- 部分网站被屏蔽
- 可能触发验证码

#### 方法 2: curl 模拟移动端

```bash
curl -s -A "Mozilla/5.0 (Linux; Android 10)" \
  -H "Accept: text/html" \
  --compressed \
  --max-time 80 \
  "<URL>"
```

**优点：**
- 直接获取原始 HTML
- 可自定义请求头
- 适合简单页面

**缺点：**
- 需要解析 HTML
- 无法执行 JavaScript

#### 方法 3: browser_use 浏览器

```javascript
browser_use.open(url)
browser_use.snapshot()
```

**优点：**
- 完整渲染页面
- 执行 JavaScript
- 可截图保存

**缺点：**
- 速度较慢
- 可能触发反爬虫

#### 方法 4: 缓存服务

```bash
# Google 缓存
curl "https://r.jina.ai/http://webcache.googleusercontent.com/search?q=cache:<URL>"

# Archive.org
curl "https://archive.org/wayback/available?url=<URL>"
```

**优点：**
- 绕过实时反爬虫
- 获取历史版本

**缺点：**
- 缓存可能过期
- 不是所有页面都有缓存

### 内容解析流程

```
1. 接收 URL
   ↓
2. 尝试 r.jina.ai
   ├─ 成功 → 提取 Markdown → 保存
   └─ 失败 → 下一步
   ↓
3. 尝试 curl 移动端
   ├─ 成功 → 解析 HTML → 保存
   └─ 失败 → 下一步
   ↓
4. 尝试 browser_use
   ├─ 成功 → 截图 + 快照 → 保存
   └─ 失败 → 下一步
   ↓
5. 尝试缓存服务
   ├─ 成功 → 提取内容 → 保存
   └─ 失败 → 报告错误
```

## 📁 文件结构

```
web_content_extractor/
├── SKILL.md              # 本文件
├── extract.sh            # 提取脚本（可选）
└── templates/
    └── archive.md        # 档案模板
```

## 💾 输出格式

### 成功提取

```markdown
# 网页内容存档

## 元数据
- **标题：** <文章标题>
- **URL：** <原始链接>
- **提取时间：** 2026-03-22 14:30:00
- **提取方法：** r.jina.ai
- **状态：** ✅ 成功

## 正文内容

<提取的文章正文>

---

## 技术信息
- 尝试次数：1
- 提取耗时：2.3s
```

### 部分成功

```markdown
# 网页内容存档（部分）

## 元数据
- **标题：** <文章标题>
- **URL：** <原始链接>
- **提取时间：** 2026-03-22 14:30:00
- **提取方法：** curl + GitHub 补充
- **状态：** ⚠️ 部分成功

## 已获取内容

<部分正文 + 相关项目信息>

## 未获取内容
- 完整正文（触发验证码）
- 图片内容

## 建议
建议用户手动复制原文内容
```

### 完全失败

```markdown
# 网页内容提取失败

## 元数据
- **URL：** <原始链接>
- **提取时间：** 2026-03-22 14:30:00
- **状态：** ❌ 失败

## 尝试记录
1. r.jina.ai - 触发验证码
2. curl - 连接超时
3. browser_use - 环境异常
4. 缓存服务 - 无记录

## 建议
1. 用户手动访问链接
2. 提供截图或复制内容
3. 稍后重试
```

## 🔍 内容解析技巧

### HTML 提取正则

```bash
# 提取标题
grep -oP '<title>\K[^<]+' 

# 提取段落
grep -oP '<p[^>]*>\K[^<]+'

# 提取链接
grep -oP 'href="\K[^"]+'

# 提取中文内容
strings | grep -oP '[\x{4e00}-\x{9fa5}]+'
```

### Markdown 清理

```bash
# 移除多余空行
sed '/^$/N;/^\n$/D'

# 标准化标题
sed 's/^####*/## /g'
```

## 🛡️ 安全和伦理

### 使用限制

1. **尊重 robots.txt** - 检查网站爬虫政策
2. **频率限制** - 避免短时间内大量请求
3. **版权保护** - 仅用于个人学习和分析
4. **隐私保护** - 不提取敏感个人信息

### 最佳实践

- 优先使用官方 API
- 添加合理的 User-Agent
- 设置请求间隔
- 缓存已提取内容
- 明确标注来源

## 📝 使用示例

### 示例 1: 微信公众号文章

```
用户：读取这篇微信文章 https://mp.weixin.qq.com/s/xxx

助手：
🔄 正在提取网页内容...
✓ 方法 1: r.jina.ai - 触发验证，尝试下一方法
✓ 方法 2: curl 移动端 - 获取部分 HTML
✓ 方法 3: GitHub 搜索 - 找到相关项目
✓ 方法 4: 整合信息 - 完成

📄 已提取内容：
- 标题：OpenClaw 玩家有福了！...
- 安装命令：git clone ...
- 相关项目：6 个 GitHub 仓库

💾 已保存到：memory/wechat_article_archive_xxx.md
```

### 示例 2: 技术博客

```
用户：帮我看看这篇教程 https://example.com/tutorial

助手：
🔄 正在提取网页内容...
✓ 方法 1: r.jina.ai - 成功提取 Markdown

📄 文章概要：
- 标题：Complete Guide to ...
- 字数：约 3000 字
- 主要话题：...

💾 已保存到：memory/article_archive_example.md
```

### 示例 3: 新闻文章

```
用户：保存这篇新闻 https://news.example.com/article/123

助手：
🔄 正在提取网页内容...
✓ 方法 1: r.jina.ai - 成功

📄 新闻摘要：
- 标题：...
- 发布时间：...
- 关键信息：...

💾 已保存到：memory/news_archive_123.md
```

## 🔄 更新日志

- **v1.0** (2026-03-22) - 初始版本
  - 多策略提取
  - 自动 fallback
  - 内容固化
  - 微信特殊支持

## 📞 故障排除

### 常见问题

**Q: 所有方法都失败怎么办？**
A: 建议用户手动复制内容，或稍后重试。

**Q: 提取的内容不完整？**
A: 检查是否触发反爬虫，尝试使用缓存服务。

**Q: 中文乱码？**
A: 使用 `iconv` 转换编码，或指定 UTF-8。

**Q: 保存失败？**
A: 检查 `memory/` 目录权限，确保可写。

## 🎓 进阶用法

### 批量提取

```bash
# 从文件读取 URL 列表
while read url; do
  ./extract.sh "$url"
done < urls.txt
```

### 定时抓取

```bash
# 添加 cron 任务
0 */6 * * * /path/to/extract.sh <url>
```

### API 集成

可以封装为 HTTP API 供其他服务调用。

---

**技能创建者：** 如意 (Ruyi)
**创建时间：** 2026-03-22
**版本：** 1.0
