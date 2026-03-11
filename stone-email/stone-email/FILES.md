# stone-email Skill 文件清单

## 核心文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 说明文档（OpenClaw 识别） |
| `_meta.json` | 技能元数据 |
| `email_tool.py` | 核心工具代码（Python） |
| `package.json` | Node.js 依赖配置 |

## 配置文件

| 文件 | 说明 | 是否公开 |
|------|------|---------|
| `config.json` | 邮箱配置（含敏感信息） | ❌ 否（已忽略） |
| `config.example.json` | 配置示例模板 | ✅ 是 |

## 文档

| 文件 | 说明 |
|------|------|
| `README.md` | 完整使用文档 |
| `QUICKSTART.md` | 快速入门指南 |
| `SKILL.md` | Skill 定义和命令参考 |

## 目录结构

| 目录 | 说明 |
|------|------|
| `bin/` | 可执行脚本（命令行入口） |
| `scripts/` | 辅助脚本（初始化、测试等） |
| `templates/` | HTML 邮件模板 |

## 其他

| 文件 | 说明 |
|------|------|
| `.gitignore` | Git 忽略规则（保护敏感配置） |

---

## GitHub 仓库

- **仓库地址**: https://github.com/hao65103940/clawskillsvault
- **技能路径**: `stone-email/`

## 安装方式

### 方式 1：从 GitHub 克隆（推荐）

```bash
cd /path/to/your/skills
git clone https://github.com/hao65103940/clawskillsvault.git stone-email
cd stone-email
npm install
cp config.example.json config.json
# 编辑 config.json 填入邮箱信息
```

### 方式 2：使用 ClawHub（如果已发布）

```bash
npx skills add stone-email
cd skills/stone-email
npm run init
```

---

**版本**: 1.0.0  
**最后更新**: 2026-03-10
