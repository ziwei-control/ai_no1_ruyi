# 🌐 Web Content Extractor - 快速使用卡片

## 🎯 一句话说明

**智能提取网页内容，自动保存到本地档案**

---

## 🚀 3 秒上手

### 方式 1: 对话中使用（推荐）

```
用户：帮我读取这篇文章
https://example.com/article

助手：🔄 正在提取...
📄 已保存：memory/web_archive_*.md
```

### 方式 2: 命令行

```bash
cd /root/.copaw/skills/web_content_extractor
./extract.sh "https://example.com"
```

---

## 📊 提取策略（自动选择）

| 方法 | 优先级 | 适用场景 |
|------|--------|----------|
| 🥇 r.jina.ai | 1️⃣ | 普通网页（最快） |
| 🥈 curl 移动端 | 2️⃣ | 微信公众号/知乎 |
| 🥉 browser_use | 3️⃣ | 动态 JS 内容 |
| 4️⃣ GitHub 搜索 | 4️⃣ | 技术文章补充 |
| 5️⃣ 缓存服务 | 5️⃣ | 备用方案 |

---

## 💡 典型场景

### ✅ 适合

- 技术博客文章
- 新闻网页
- GitHub README
- 文档教程
- 微信公众号（部分）

### ⚠️ 限制

- 强反爬虫网站（需手动）
- 付费墙内容
- 需要登录的内容
- 视频/音频内容

---

## 📁 输出示例

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
```

---

## 🔧 高级用法

### 带关键词（GitHub 补充）

```bash
./extract.sh "https://mp.weixin.qq.com/s/xxx" "OpenClaw Dashboard"
```

### 批量提取

```bash
while read url; do
  ./extract.sh "$url"
  sleep 3
done < urls.txt
```

---

## 📚 完整文档

| 文件 | 内容 |
|------|------|
| `README.md` | 快速开始指南 |
| `SKILL.md` | 完整技术文档 |
| `EXAMPLES.md` | 使用示例 |
| `创建总结.md` | 创建过程记录 |

---

## ⚠️ 使用准则

- ✅ 仅用于学习研究
- ✅ 尊重 robots.txt
- ✅ 控制请求频率
- ❌ 不用于商业用途
- ❌ 不提取敏感信息

---

## 📞 故障排除

| 问题 | 解决 |
|------|------|
| 全部失败 | 检查网络，稍后重试 |
| 中文乱码 | 手动访问复制 |
| 文件过大 | 限制内容长度 |
| 卡住不动 | 使用 timeout 命令 |

---

## 🎯 最佳实践

1. **优先 r.jina.ai** - 最快最干净
2. **提供关键词** - 帮助 GitHub 搜索
3. **检查存档** - 确认完整性
4. **手动补充** - 必要时复制原文

---

## 📍 文件位置

```
技能目录：/root/.copaw/skills/web_content_extractor/
存档目录：/root/.copaw/memory/web_archive_*.md
记忆文件：/root/.copaw/MEMORY.md（已更新）
```

---

**版本：** 1.0 | **创建：** 2026-03-22 | **维护：** 如意 (Ruyi)
