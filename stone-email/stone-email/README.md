# stone-email 📧

通用邮件收发 Skill for OpenClaw - 支持腾讯/网易/Gmail/QQ 等主流邮箱

## ✨ 功能特性

- ✅ **读取邮件** - IMAP 协议接收邮件，支持批量读取
- ✅ **发送邮件** - SMTP 协议发送邮件
- ✅ **多收件人** - 支持多个收件人、抄送 (CC)、密送 (BCC)
- ✅ **附件支持** - 发送和查看附件
- ✅ **HTML 模板** - 支持 HTML 邮件和模板渲染
- ✅ **多服务商** - 腾讯企业邮、网易企业邮、163、Gmail、QQ 邮箱等

## 📦 安装

### 方式 1: 从 GitHub 克隆（推荐）

```bash
cd /path/to/your/skills
git clone https://github.com/hao65103940/clawskillsvault.git stone-email
cd stone-email
npm install
```

### 方式 2: 使用 ClawHub（如果已发布）

```bash
npx skills add stone-email
```

## 🚀 快速开始

### 1. 初始化配置

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置文件
vim config.json
```

### 2. 配置邮箱信息

编辑 `config.json`，填入你的邮箱信息：

```json
{
  "email": "your-email@example.com",
  "password": "your-auth-code-or-password",
  "imap_server": "imap.example.com",
  "imap_port": 993,
  "smtp_server": "smtp.example.com",
  "smtp_port": 587,
  "provider": "tencent"
}
```

### 3. 测试连接

```bash
npm run test
```

## 📋 使用示例

### 读取邮件

**读取最新 10 封邮件：**
```bash
python3 email_tool.py read --limit 10
```

**读取指定邮件（通过 UID）：**
```bash
python3 email_tool.py read --uid 123 --full
```

**查看邮件附件：**
```bash
python3 email_tool.py read --uid 123 --attachments
```

### 发送邮件

**发送纯文本邮件：**
```bash
python3 email_tool.py send \
  --to recipient@example.com \
  --subject "邮件主题" \
  --text "邮件正文内容"
```

**发送多个收件人：**
```bash
python3 email_tool.py send \
  --to a@example.com b@example.com c@example.com \
  --subject "主题" \
  --text "正文"
```

**带抄送和密送：**
```bash
python3 email_tool.py send \
  --to a@example.com b@example.com \
  --cc manager@example.com \
  --bcc backup@example.com \
  --subject "主题" \
  --text "正文"
```

**发送带附件：**
```bash
python3 email_tool.py send \
  --to recipient@example.com \
  --subject "报告" \
  --text "请查收附件" \
  --attach /path/to/file.pdf
```

**发送 HTML 邮件：**
```bash
python3 email_tool.py send \
  --to recipient@example.com \
  --subject "主题" \
  --html "<h1>HTML 内容</h1><p>正文</p>"
```

**使用 HTML 模板：**
```bash
python3 email_tool.py send \
  --to recipient@example.com \
  --subject "主题" \
  --text "纯文本版本（备用）" \
  --template templates/default.html \
  --var "greeting=你好！" \
  --var "content=邮件正文内容" \
  --var "button=true" \
  --var "button_text=点击查看" \
  --var "button_link=https://example.com"
```

## 🏢 支持的邮箱服务商

| 服务商 | IMAP 服务器 | SMTP 服务器 | 说明 |
|--------|------------|------------|------|
| **腾讯企业邮** | `imap.exmail.qq.com:993` | `smtp.exmail.qq.com:587` | 企业微信邮箱 |
| **网易企业邮** | `imap.qiye.163.com:993` | `smtp.qiye.163.com:587` | 163 企业邮箱 |
| **163 邮箱** | `imap.163.com:993` | `smtp.163.com:587` | 个人 163 邮箱 |
| **QQ 邮箱** | `imap.qq.com:993` | `smtp.qq.com:587` | QQ 个人邮箱 |
| **Gmail** | `imap.gmail.com:993` | `smtp.gmail.com:587` | 需要开启 IMAP |
| **Outlook** | `outlook.office365.com:993` | `smtp.office365.com:587` | Office 365 |

## 🔒 安全说明

### 配置文件安全

- ✅ `config.json` 已加入 `.gitignore`，不会被提交到 Git
- ✅ 建议设置文件权限：`chmod 600 config.json`
- ⚠️ **切勿**将 `config.json` 上传到公开代码库
- ⚠️ 建议使用**授权码**而非登录密码

### 获取授权码

**腾讯企业邮：**
1. 登录企业邮网页版
2. 设置 → 客户端设置
3. 开启 IMAP/SMTP 服务
4. 生成授权码

**QQ 邮箱：**
1. 登录 QQ 邮箱网页版
2. 设置 → 账户
3. 开启 POP3/SMTP 服务
4. 生成授权码

**Gmail：**
1. 开启两步验证
2. 生成应用专用密码
3. 使用应用专用密码作为授权码

## 📁 文件结构

```
stone-email/
├── SKILL.md              # Skill 定义文件
├── README.md             # 使用说明（本文件）
├── QUICKSTART.md         # 快速入门指南
├── FILES.md              # 文件清单
├── package.json          # NPM 配置
├── config.example.json   # 配置模板（安全）
├── config.json           # 实际配置（需创建，已忽略）
├── email_tool.py         # 核心邮件工具脚本
├── .gitignore            # Git 忽略配置
├── bin/
│   └── email             # 命令行入口脚本
├── scripts/
│   ├── init.js           # 初始化向导
│   └── test-connection.js # 连接测试脚本
└── templates/
    └── default.html      # HTML 邮件模板
```

## 🆘 故障排除

### IMAP/SMTP 连接失败

**错误信息：** `Login fail` 或 `Authentication failed`

**解决方案：**
1. 检查邮箱地址是否正确
2. 检查授权码是否正确（不是登录密码）
3. 确认邮箱已开启 IMAP/SMTP 服务
4. 检查 IMAP/SMTP 服务器地址和端口
5. 检查网络连接和防火墙设置

### 找不到配置文件

**错误信息：** `Config file not found`

**解决方案：**
```bash
# 创建配置文件
cp config.example.json config.json
# 编辑 config.json 填入邮箱信息
```

### 附件发送失败

**解决方案：**
1. 检查文件路径是否正确（使用绝对路径）
2. 确认文件存在且可读
3. 检查附件大小（通常限制 25MB 以内）

### HTML 模板渲染失败

**解决方案：**
1. 检查模板路径是否正确
2. 确保模板文件存在
3. 检查变量名是否匹配

## 🔧 高级配置

### 自定义配置路径

可以通过环境变量指定配置文件路径：

```bash
export STONE_EMAIL_CONFIG=/path/to/your/config.json
python3 email_tool.py read --limit 10
```

### 日志调试

启用详细日志输出：

```bash
python3 email_tool.py read --limit 10 --debug
```

## 📞 支持与反馈

- **GitHub 仓库：** https://github.com/hao65103940/clawskillsvault
- **提交 Issue：** https://github.com/hao65103940/clawskillsvault/issues
- **讨论区：** https://github.com/hao65103940/clawskillsvault/discussions

## 📄 License

MIT License - 详见 LICENSE 文件

---

**作者：** AI Assistant  
**版本：** 1.0.0  
**最后更新：** 2026-03-10
