# 快速开始指南 📧

## 3 分钟上手

### 1️⃣ 安装

**方式 A：从 GitHub 克隆（推荐）**
```bash
cd /path/to/your/skills
git clone https://github.com/hao65103940/clawskillsvault.git stone-email
cd stone-email
npm install
```

**方式 B：使用 ClawHub（如果已发布）**
```bash
npx skills add stone-email
cd skills/stone-email
```

### 2️⃣ 配置

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置文件，填入你的邮箱信息
vim config.json
```

**配置示例：**
```json
{
  "email": "your-email@example.com",
  "password": "your-auth-code",
  "imap_server": "imap.exmail.qq.com",
  "imap_port": 993,
  "smtp_server": "smtp.exmail.qq.com",
  "smtp_port": 587,
  "provider": "tencent"
}
```

### 3️⃣ 测试

```bash
# 测试连接
npm run test

# 或发送测试邮件
python3 email_tool.py send \
  --to your-email@example.com \
  --subject "测试邮件" \
  --text "这是测试邮件"
```

### 4️⃣ 使用

```bash
# 读取邮件
python3 email_tool.py read --limit 10

# 发送邮件
python3 email_tool.py send \
  --to someone@example.com \
  --subject "你好" \
  --text "这是一封邮件"
```

---

## 常用命令

### 📥 读取邮件

```bash
# 最新 10 封
python3 email_tool.py read --limit 10

# 指定邮件（通过 UID）
python3 email_tool.py read --uid 123 --full

# 查看附件
python3 email_tool.py read --uid 123 --attachments
```

### 📤 发送邮件

```bash
# 简单发送
python3 email_tool.py send --to xxx@example.com --subject "主题" --text "正文"

# 多收件人
python3 email_tool.py send --to a@example.com b@example.com --subject "主题" --text "正文"

# 带抄送
python3 email_tool.py send --to a@example.com --cc b@example.com --subject "主题" --text "正文"

# 带附件
python3 email_tool.py send --to xxx@example.com --subject "主题" --text "正文" --attach file.pdf

# HTML 模板
python3 email_tool.py send --to xxx@example.com --subject "主题" --template templates/default.html
```

---

## 配置示例

### 腾讯企业邮
```json
{
  "email": "you@example.com",
  "password": "your-auth-code",
  "imap_server": "imap.exmail.qq.com",
  "imap_port": 993,
  "smtp_server": "smtp.exmail.qq.com",
  "smtp_port": 587,
  "provider": "tencent"
}
```

### Gmail
```json
{
  "email": "you@gmail.com",
  "password": "your-app-password",
  "imap_server": "imap.gmail.com",
  "imap_port": 993,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "provider": "gmail"
}
```

### 163 邮箱
```json
{
  "email": "you@163.com",
  "password": "your-auth-code",
  "imap_server": "imap.163.com",
  "imap_port": 993,
  "smtp_server": "smtp.163.com",
  "smtp_port": 587,
  "provider": "163"
}
```

### QQ 邮箱
```json
{
  "email": "you@qq.com",
  "password": "your-auth-code",
  "imap_server": "imap.qq.com",
  "imap_port": 993,
  "smtp_server": "smtp.qq.com",
  "smtp_port": 587,
  "provider": "qq"
}
```

---

## 下一步

- 📖 完整文档：[README.md](README.md)
- 🔧 高级用法：[SKILL.md](SKILL.md)
- 🐛 问题反馈：[GitHub Issues](https://github.com/hao65103940/clawskillsvault/issues)
