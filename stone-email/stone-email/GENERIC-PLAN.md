# stone-email Skill 开发计划

## 📋 改造清单

### ✅ 已完成

| 项目 | 文件 | 说明 |
|------|------|------|
| ✅ 配置分离 | `config.json` | 邮箱配置独立文件 |
| ✅ 配置模板 | `config.example.json` | 用户复制修改 |
| ✅ 初始化向导 | `scripts/init.js` | 交互式配置 |
| ✅ 连接测试 | `scripts/test-connection.js` | 测试 IMAP/SMTP |
| ✅ 配置加载 | `email_tool.py` | 自动加载 config.json |
| ✅ 权限保护 | `chmod 600` | 敏感文件保护 |
| ✅ Git 忽略 | `.gitignore` | 不提交配置 |
| ✅ NPM 配置 | `package.json` | 支持 npm install |
| ✅ 快速开始 | `QUICKSTART.md` | 3 分钟上手 |
| ✅ 更新文档 | `README.md` | 完整使用说明 |
| ✅ 更新 SKILL | `SKILL.md` | 添加安装步骤 |
| ✅ 统一命名 | 全部文件 | `stone-email` 前缀 |
| ✅ 敏感信息清理 | 全部文件 | 移除真实邮箱和授权码 |

---

## 📦 发布到 ClawHub

### 1. GitHub 仓库状态

```bash
cd /path/to/stone-email
git status
git log --oneline -5
```

### 2. 发布到 ClawHub（可选）

```bash
npx clawhub publish /path/to/stone-email
```

### 3. 用户安装

```bash
# 方式 1：从 GitHub 克隆
cd /path/to/your/skills
git clone https://github.com/hao65103940/clawskillsvault.git stone-email
cd stone-email
npm install
cp config.example.json config.json
# 编辑 config.json 填入邮箱信息

# 方式 2：从 ClawHub 安装（如果已发布）
npx skills add stone-email
cd skills/stone-email
npm install
npm run init
```

---

## 🔧 配置路径

### 配置文件搜索顺序

`email_tool.py` 会按以下顺序查找配置文件：

1. `./config.json` - 脚本同目录
2. `~/.stone-email/config.json` - 用户目录
3. `./config.json` - 当前工作目录

### 多环境配置

可以为不同环境创建不同配置：

```bash
# 开发环境
cp config.example.json config.dev.json

# 生产环境
cp config.example.json config.prod.json

# 使用时指定
export STONE_EMAIL_CONFIG=/path/to/config.prod.json
```

---

## 📝 待办事项

### 功能增强

- [ ] 支持 OAuth2 认证（Gmail/Outlook）
- [ ] 支持邮件搜索和过滤
- [ ] 支持邮件标记（已读/星标等）
- [ ] 支持邮件删除和移动
- [ ] 支持多个邮箱账户切换

### 文档完善

- [ ] 添加视频教程
- [ ] 添加常见问题 FAQ
- [ ] 添加更多服务商配置示例
- [ ] 添加 API 参考文档

### 测试

- [ ] 单元测试
- [ ] 集成测试
- [ ] CI/CD 配置

---

## 🎯 目标

打造一个**通用、安全、易用**的邮件 Skill，让用户能够：

1. **3 分钟上手** - 快速配置，立即使用
2. **多服务商支持** - 腾讯、网易、Gmail、QQ 等
3. **安全可靠** - 配置隔离，敏感信息保护
4. **功能完整** - 收发邮件、附件、HTML 模板

---

**版本**: 1.0.0  
**最后更新**: 2026-03-10
