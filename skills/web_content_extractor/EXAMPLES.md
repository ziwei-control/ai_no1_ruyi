# Web Content Extractor - 使用示例

## 🎯 快速开始

### 方法 1: 自动触发

当用户提供 URL 时，助手会自动使用此技能：

```
用户：帮我读取这篇文章
https://mp.weixin.qq.com/s/fr9vs8pEc8wRGcwKhtMgOw

助手：🔄 正在提取网页内容...
[自动执行提取流程]
```

### 方法 2: 手动调用脚本

```bash
cd /root/.copaw/skills/web_content_extractor

# 基本用法
./extract.sh "https://example.com/article"

# 带关键词（用于 GitHub 搜索补充）
./extract.sh "https://mp.weixin.qq.com/s/xxx" "OpenClaw Dashboard"
```

### 方法 3: 在对话中明确提及

```
用户：使用 web_content_extractor 技能读取 https://...
```

## 📝 实际案例

### 案例 1: 微信公众号文章

**输入：**
```
读取这篇微信文章：
https://mp.weixin.qq.com/s/fr9vs8pEc8wRGcwKhtMgOw
```

**执行流程：**
1. 尝试 r.jina.ai → 触发验证 ❌
2. 尝试 curl 移动端 → 获取部分 HTML ⚠️
3. 提取关键词 "OpenClaw Dashboard" → GitHub 搜索 ✅
4. 整合信息 → 生成档案 ✅

**输出：**
```
📄 存档位置：/root/.copaw/memory/web_archive_mp_weixin_qq_com_20260322_143000.md
📊 提取方法：curl 移动端模拟 + GitHub 搜索
📋 状态：⚠️ 部分成功

已获取：
- 文章标题
- 安装命令
- 相关 GitHub 项目信息

建议：手动复制完整原文
```

### 案例 2: 技术博客

**输入：**
```
帮我看看这篇教程：
https://juejin.cn/post/123456789
```

**执行流程：**
1. 尝试 r.jina.ai → 成功 ✅
2. 提取 Markdown 内容
3. 生成档案

**输出：**
```
📄 存档位置：/root/.copaw/memory/web_archive_juejin_cn_20260322_145000.md
📊 提取方法：r.jina.ai API
📋 状态：✅ 成功

文章概要：
- 标题：Complete Guide to XXX
- 字数：约 3000 字
- 主要话题：...
```

### 案例 3: GitHub 项目

**输入：**
```
读取这个项目的 README：
https://github.com/openclaw/openclaw
```

**执行流程：**
1. 尝试 r.jina.ai → 成功 ✅
2. 获取 README Markdown
3. 生成档案

## 🔧 高级用法

### 批量提取

创建 `urls.txt` 文件：
```
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

执行批量提取：
```bash
while read url; do
  ./extract.sh "$url"
done < urls.txt
```

### 定时抓取

添加到 crontab：
```bash
# 每 6 小时抓取一次
0 */6 * * * /root/.copaw/skills/web_content_extractor/extract.sh "https://example.com/feed"
```

### 自定义配置

编辑 `extract.sh` 修改配置：
```bash
# 修改超时时间
TIMEOUT_LONG=90  # 原为 60 秒

# 修改存档目录
MEMORY_DIR="/path/to/custom/memory"
```

## 📊 输出格式

### 成功提取的档案结构

```markdown
# 网页内容存档

## 元数据
- **URL：** https://...
- **提取时间：** 2026-03-22 14:30:00
- **提取方法：** r.jina.ai API
- **状态：** ✅ 成功

---

## 正文内容

[提取的文章正文]

---

## 技术信息
- 生成时间：...
- 存档位置：...
```

### 部分成功的档案结构

```markdown
# 网页内容存档（部分）

## 元数据
- **URL：** https://...
- **提取时间：** ...
- **提取方法：** curl + GitHub
- **状态：** ⚠️ 部分成功

---

## 已获取内容

[部分正文 + 相关项目信息]

---

## 未获取内容
- 完整正文（触发验证码）
- 图片内容

## 建议
建议用户手动复制原文内容
```

## 🛠️ 故障排除

### 问题 1: 所有方法都失败

**症状：** 显示 ❌ 失败

**解决方案：**
1. 检查网络连接
2. 手动访问 URL 确认网站正常
3. 稍后重试
4. 建议用户提供截图或复制内容

### 问题 2: 中文乱码

**症状：** 提取内容显示乱码

**解决方案：**
```bash
# 手动指定编码转换
curl ... | iconv -f gb2312 -t utf-8
```

### 问题 3: 存档文件过大

**症状：** 生成的文件超过 10MB

**解决方案：**
1. 修改脚本限制内容长度
2. 只提取前 N 个段落
3. 压缩存档文件

## 📈 性能优化

### 加速提取

1. **优先使用 r.jina.ai** - 最快最干净
2. **设置合理超时** - 避免长时间等待
3. **缓存已提取内容** - 避免重复提取

### 提高成功率

1. **多种方法组合** - 自动 fallback
2. **移动端 UA** - 绕过部分反爬虫
3. **GitHub 补充** - 获取相关项目信息

## 🔐 安全和伦理

### 使用准则

- ✅ 仅用于个人学习和研究
- ✅ 尊重网站 robots.txt
- ✅ 控制请求频率
- ✅ 标注内容来源
- ❌ 不用于商业用途
- ❌ 不提取敏感信息
- ❌ 不大量爬取

### 最佳实践

```bash
# 添加请求延迟
sleep 2  # 每个请求间隔 2 秒

# 限制每日提取数量
MAX_DAILY=50
```

## 📚 相关文件

- `SKILL.md` - 技能完整文档
- `extract.sh` - 提取脚本
- `EXAMPLES.md` - 本文件
- `memory/*.md` - 生成的档案

## 🎓 学习资源

- [r.jina.ai 文档](https://r.jina.ai/)
- [curl 官方文档](https://curl.se/docs/)
- [Web Scraping 最佳实践](https://scrapinghub.com/web-scraping-101)

---

**创建时间：** 2026-03-22
**版本：** 1.0
**维护者：** 如意 (Ruyi)
