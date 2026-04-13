---
name: add-agent
description: 批量创建新的独立 agent，配置独立工作空间、模型、企微绑定和 exec 权限
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["openclaw"]}}}
---

## 功能

批量根据用户提供的多个 agent 信息，自动完成以下配置：
1. 使用 `openclaw agents add` 命令批量创建 agent（命令自动创建 workspace + bootstrap 文件 + bindings）
2. 修复 bindings 配置（移除多余的 type 字段）
3. 批量添加 tools 配置
4. 批量添加企微 Bot 配置
5. 批量更新 exec-approvals.json
6. 批量同步工作空间技能

## 使用方式

用户可以一次性提供多个 agent 的信息，格式如下：

### 输入格式

```
添加 agent:
1. agentID: alice, BotID: xxx, Secret: yyy, 模型: glm-5, 命令: /usr/bin/python3
2. agentID: bob, BotID: aaa, Secret: bbb, 模型: qwen3.5-plus
```

或者更简洁：
```
批量添加:
- alice, botId: xxx, secret: yyy
- bob, botId: aaa, secret: bbb, 模型: glm-5
- charlie, botId: ccc, secret: ddd, 命令: /usr/bin/python3, /usr/bin/curl
```

### 用户需要提供（每个 agent）

- **agent ID**：英文标识
- **企微 BotID**：企业微信后台获取的 botId
- **企微 Secret**：企业微信后台获取的 secret
- **模型**：（可选，默认使用 `bailian/qwen3.5-plus`）
- **允许执行的命令**：（可选，默认 `/usr/bin/python3`, `/usr/local/bin/python3`）

## 执行步骤

### ⚠️ 重要：必须使用命令创建 agent

**禁止直接修改 JSON 文件创建 agent**，必须使用 `openclaw agents add` 命令！

### 第一步：解析用户输入

解析用户提供的多个 agent 信息，提取每个 agent 的：
- agent ID
- BotID
- Secret
- 模型
- 允许命令列表

### 第二步：检查是否已存在

对每个 agent 检查：
- `agents.list` 中是否有相同 id
- `channels.wecom.accounts` 中是否有相同的 botId

如果存在，提示用户确认是否覆盖。

### 第三步：使用 openclaw agents add 命令创建 agent

对每个 agent 执行：

```bash
openclaw agents add <agentId> \
  --workspace /opt/openclaw-subagents/workspace-<agentId>/ \
  --bind wecom:<agentId> \
  --model <model> \
  --non-interactive
```

**命令会自动完成以下操作**：
- ✅ 创建 workspace 目录
- ✅ 自动生成 bootstrap 文件（AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, TOOLS.md, IDENTITY.md, BOOTSTRAP.md）
- ✅ 添加 agent 到 agents.list
- ✅ 添加企微 bindings（channel + accountId）
- ❌ bindings 会带有 `type: route`，需要修复

### 第四步：修复 bindings 配置

命令自动添加的 bindings 带有 `"type": "route"`，需要移除以保持格式一致。

读取 `~/.openclaw/openclaw.json`，找到新创建 agent 的 bindings，删除 `type` 字段：

```json
# 修改前
{ "type": "route", "agentId": "<agentId>", "match": { ... } }

# 修改后
{ "agentId": "<agentId>", "match": { ... } }
```

### 第五步：批量添加 tools 配置

对每个 agent，在 `agents.list` 中添加 tools 配置：

```json
{
  "tools": {
    "allow": [
      "read", "write", "edit", "apply_patch", "exec", "process",
      "memory_search", "memory_get", "cron", "message"
    ],
    "deny": [
      "browser", "gateway", "nodes", "sessions_spawn"
    ]
  }
}
```

### 第六步：批量添加企微账户配置

在 `channels.wecom.accounts` 中批量追加：

```json
"<agentId>": {
  "enabled": true,
  "name": "<agentId> Bot",
  "botId": "<botId>",
  "secret": "<secret>"
}
```

**注意**：不要添加 `connectionMode` 和 `domain` 字段。

### 第七步：批量更新 exec-approvals.json（默认完全开放）

**默认设置**：安全级别设为 full，执行所有命令不需要审批。

在 `agents` 中追加：

```json
"<agentId>": {
  "security": "full",
  "ask": "off"
}
```

**说明**：
- `security: full` - 允许执行所有命令
- `ask: off` - 不询问审批

**备选：更安全的配置（需要审批）**
```json
"<agentId>": {
  "security": "allowlist",
  "ask": "on-miss",
  "askFallback": "deny",
  "allowlist": [
    { "id": "<UUID>", "pattern": "cordys", "lastUsedAt": <timestamp> },
    { "id": "<UUID>", "pattern": "/usr/bin/python3", "lastUsedAt": <timestamp> }
  ]
}
```

### 第八步：批量同步工作空间技能（排除敏感文件）

```bash
rsync -av --delete \
  --exclude='.env' \
  --exclude='config.json' \
  --exclude='.env.*' \
  --exclude='.git/' \
  --exclude='node_modules/' \
  ~/.openclaw/workspace/skills/ /opt/openclaw-subagents/workspace-<agentId>/skills/
```

**排除规则**：
- ❌ 排除：`.env`（包含 API Key）
- ❌ 排除：`config.json`（包含密码）
- ❌ 排除：`.env.*`（如 .env.production）
- ✅ 保留：`.env.example`（模板）
- ✅ 保留：`config.example.json`（模板）

**或者使用 cp 命令（需要手动排除）**：
```bash
# 创建目标目录
mkdir -p /opt/openclaw-subagents/workspace-<agentId>/skills/

# 复制技能（排除敏感文件）
cd ~/.openclaw/workspace/skills
for skill in *; do
  if [ -d "$skill" ]; then
    # 创建技能目录
    mkdir -p "/opt/openclaw-subagents/workspace-<agentId>/skills/$skill"
    # 复制所有文件
    cp -r $skill/* "/opt/openclaw-subagents/workspace-<agentId>/skills/$skill/" 2>/dev/null || true
    # 删除敏感文件（只删实际配置，保留模板）
    rm -f "/opt/openclaw-subagents/workspace-<agentId>/skills/$skill/.env" 2>/dev/null || true
    rm -f "/opt/openclaw-subagents/workspace-<agentId>/skills/$skill/config.json" 2>/dev/null || true
    # 保留 .env.example 和 config.example.json
  fi
done
```

**注意**：
- workspace 目录和 bootstrap 文件已由命令自动创建，只需同步 skills 目录
- 必须排除敏感文件：.env, config.json, *.env, .env.*
- 同步后需验证敏感文件未同步到目标目录

### 第九步：写回配置文件

将修改后的 JSON 写回：
- `~/.openclaw/openclaw.json`
- `~/.openclaw/exec-approvals.json`

### 第十步：输出结果摘要（不重启）

输出每个 agent 的创建结果：

```
✅ 创建成功:
- alice: workspace=/opt/openclaw-subagents/workspace-alice/, model=bailian/glm-5, BotID=xxx
- bob: workspace=/opt/openclaw-subagents/workspace-bob/, model=bailian/qwen3.5-plus, BotID=aaa

⚠️ 共创建 N 个 agent，需要重启 Gateway 使配置生效
```

### 第十一步：询问是否重启

询问用户：
```
是否立即重启 Gateway 使配置生效？（是/否）
```

### 第十二步：根据用户回答执行

- **是**：执行 `openclaw gateway restart`，输出重启结果
- **否**：告知用户稍后手动执行 `openclaw gateway restart`

## 输出模板

### 创建成功时

```
🎉 批量创建完成！

| # | Agent ID | Workspace | Model | BotID | 命令 |
|---|----------|-----------|-------|-------|------|
| 1 | alice | /opt/.../workspace-alice/ | glm-5 | xxx | /usr/bin/python3 |
| 2 | bob | /opt/.../workspace-bob/ | qwen3.5-plus | aaa | 默认 |

⚠️ 共 N 个 agent 已创建，需要重启 Gateway 使配置生效

是否立即重启 Gateway？（是/否）
```

### 重启后

```
✅ Gateway 已重启，当前运行中 (pid: xxxxx)

所有 agent 已就绪！
```

## ⚠️ 关键注意事项

1. **必须使用命令创建 agent**：禁止直接修改 JSON，必须用 `openclaw agents add` 命令
2. **命令自动创建的内容**：
   - workspace 目录
   - bootstrap 文件（AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, TOOLS.md, IDENTITY.md, BOOTSTRAP.md）
   - bindings（需修复 type 字段）
3. **修复 bindings**：命令会自动添加 `type: route`，需要删除
4. **main 和 project-manager 不能被覆盖**
5. **企微账户配置不添加 connectionMode 和 domain**
6. **默认命令**：`/usr/bin/python3`, `/usr/local/bin/python3`
7. **默认模型**：`bailian/qwen3.5-plus`
8. **每次创建后都要验证**：检查 agents.list、bindings、企微账户是否正确