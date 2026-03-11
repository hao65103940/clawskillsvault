---
name: stone-email
version: 1.0.0
description: 通用邮件收发工具 - 支持腾讯/网易/Gmail 等，多收件人、抄送、HTML 模板、附件
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins: ["python3", "node"]
      env: ["config.json"]
    os:
      - linux
      - darwin
    install:
      - id: npm-deps
        kind: node
        package: "."
        label: Install email dependencies
      - id: init-config
        kind: script
        script: node scripts/init.js
        label: Initialize email config
---

# 邮箱 Skill 📧

完整的邮件收发工具，支持腾讯企业邮、网易企业邮、Gmail、QQ 邮箱等主流邮箱服务商。

## 功能

- ✅ **读取邮件** - IMAP 协议接收邮件
- ✅ **发送邮件** - SMTP 协议发送邮件
- ✅ **多收件人** - 支持多个收件人、抄送、密送
- ✅ **附件支持** - 发送和查看附件
- ✅ **HTML 模板** - 支持 HTML 邮件和模板渲染
- ✅ **多邮件管理** - 批量读取、指定 UID 读取

## 配置

首次使用需要配置邮箱信息：

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

**常见服务商配置：**
| 服务商 | IMAP | SMTP |
|--------|------|------|
| 腾讯企业邮 | `imap.exmail.qq.com:993` | `smtp.exmail.qq.com:587` |
| 网易企业邮 | `imap.qiye.163.com:993` | `smtp.qiye.163.com:587` |
| 163 邮箱 | `imap.163.com:993` | `smtp.163.com:587` |
| QQ 邮箱 | `imap.qq.com:993` | `smtp.qq.com:587` |
| Gmail | `imap.gmail.com:993` | `smtp.gmail.com:587` |

## 命令

### 📥 读取邮件

**读取最新邮件**：
```bash
python3 email_tool.py read --limit 10
```

**读取指定邮件**：
```bash
python3 email_tool.py read --uid 123 --full
```

**查看邮件附件**：
```bash
python3 email_tool.py read --uid 123 --attachments
```

### 📤 发送邮件

**发送纯文本**：
```bash
python3 email_tool.py send --to xxx@xxx.com --subject "主题" --text "正文"
```

**发送多个收件人**：
```bash
python3 email_tool.py send \
  --to a@xxx.com b@xxx.com c@xxx.com \
  --subject "主题" \
  --text "正文"
```

**带抄送和密送**：
```bash
python3 email_tool.py send \
  --to a@xxx.com b@xxx.com \
  --cc manager@xxx.com \
  --bcc backup@xxx.com \
  --subject "主题" \
  --text "正文"
```

**发送带附件**：
```bash
python3 email_tool.py send \
  --to xxx@xxx.com \
  --subject "报告" \
  --text "请查收" \
  --attach /path/to/file.pdf
```

**发送 HTML 邮件**：
```bash
python3 email_tool.py send \
  --to xxx@xxx.com \
  --subject "主题" \
  --html "<h1>HTML 内容</h1>"
```

**使用 HTML 模板**：
```bash
python3 email_tool.py send \
  --to xxx@xxx.com \
  --subject "主题" \
  --text "纯文本版本" \
  --template templates/default.html \
  --var "greeting=你好！" \
  --var "content=邮件正文内容" \
  --var "button=true" \
  --var "button_text=点击查看" \
  --var "button_link=https://example.com"
```

## 自然语言调用

在 OpenClaw 中直接用自然语言调用：

**读取邮件**：
- "帮我读一下最新邮件"
- "看看有没有新邮件"
- "读取 UID 为 123 的邮件"
- "查看这封邮件的附件"

**发送邮件**：
- "给 xxx@xxx.com 发个邮件，主题是 XXX，内容是 XXX"
- "发个邮件给 XXX，带上这个附件"
- "回复刚才那封邮件"

## 输出格式

**读取邮件输出**：
```
📧 找到 X 封邮件:

1. 来自：xxx@xxx.com
   主题：邮件主题
   日期：Thu, 5 Mar 2026 17:12:48 +0800
   UID: 123
   📎 附件：2 个
   正文：邮件正文前 200 字...
```

**发送邮件输出**：
```
📤 发送邮件到：xxx@xxx.com
   主题：邮件主题
   📎 附件：filename.pdf
✅ 发送成功！
```

## 安全说明

- 🔐 授权码存储在 `config.json` 中，请勿外泄
- ⚠️ 不要将 `config.json` 提交到公开代码库
- 📁 建议设置文件权限：`chmod 600 config.json`
- ✅ `.gitignore` 已配置，自动忽略 `config.json`

## 故障排除

**IMAP 连接失败**：
- 检查授权码是否正确（不是登录密码）
- 确认邮箱已开启 IMAP 服务
- 检查网络连接

**SMTP 发送失败**：
- 检查授权码是否正确
- 确认邮箱已开启 SMTP 服务
- 检查收件人地址是否正确

**附件发送失败**：
- 检查文件路径是否正确（使用绝对路径）
- 确认文件存在且可读
- 附件大小限制（通常 25MB）

## 相关文件

- 工具脚本：`email_tool.py`
- 配置文件：`config.json`（需自行创建）
- 配置模板：`config.example.json`
- HTML 模板：`templates/default.html`

---

**作者**: AI Assistant  
**版本**: 1.0.0  
**License**: MIT
