#!/usr/bin/env node
/**
 * 邮件 Skill 初始化向导
 * 用法：node scripts/init.js
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_PATH = path.join(__dirname, '../config.json');
const TEMPLATE_CONFIG = {
  email: "",
  password: "",
  imap_server: "imap.exmail.qq.com",
  imap_port: 993,
  smtp_server: "smtp.exmail.qq.com",
  smtp_port: 587,
  provider: "tencent"
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

async function init() {
  console.log('\n📧 邮件 Skill 初始化向导\n');
  console.log('这将帮助你配置邮箱连接信息。\n');

  // 检查是否已有配置
  if (fs.existsSync(CONFIG_PATH)) {
    const existing = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    console.log(`⚠️  发现现有配置：${existing.email || 'unknown'}`);
    const overwrite = await ask('是否覆盖现有配置？(y/N): ');
    if (overwrite.toLowerCase() !== 'y') {
      console.log('❌ 已取消');
      rl.close();
      return;
    }
  }

  // 收集配置
  console.log('\n--- 邮箱配置 ---\n');
  
  const email = await ask('邮箱地址：');
  const password = await ask('授权码/密码（不会显示）：');
  
  // 隐藏密码输入
  process.stdin.setRawMode(true);
  process.stdin.resume();
  const passwordChars = [];
  process.stdin.on('data', (key) => {
    if (key[0] === 13) { // Enter
      process.stdin.setRawMode(false);
      process.stdin.pause();
    } else if (key[0] === 3) { // Ctrl+C
      process.exit();
    } else {
      passwordChars.push(key);
      process.stdout.write('*');
    }
  });

  const provider = await ask('\n邮箱服务商 (tencent/netease/163/gmail) [tencent]: ');
  const imapServer = await ask(`IMAP 服务器 [${TEMPLATE_CONFIG.imap_server}]: `);
  const imapPort = await ask(`IMAP 端口 [${TEMPLATE_CONFIG.imap_port}]: `);
  const smtpServer = await ask(`SMTP 服务器 [${TEMPLATE_CONFIG.smtp_server}]: `);
  const smtpPort = await ask(`SMTP 端口 [${TEMPLATE_CONFIG.smtp_port}]: `);

  // 构建配置
  const config = {
    email: email.trim(),
    password: password.trim() || TEMPLATE_CONFIG.password,
    imap_server: imapServer.trim() || TEMPLATE_CONFIG.imap_server,
    imap_port: parseInt(imapPort) || TEMPLATE_CONFIG.imap_port,
    smtp_server: smtpServer.trim() || TEMPLATE_CONFIG.smtp_server,
    smtp_port: parseInt(smtpPort) || TEMPLATE_CONFIG.smtp_port,
    provider: provider.trim() || 'tencent'
  };

  // 保存配置
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  fs.chmodSync(CONFIG_PATH, 0o600); // 仅所有者可读写

  console.log('\n✅ 配置已保存！\n');
  console.log(`📧 邮箱：${config.email}`);
  console.log(`📥 IMAP: ${config.imap_server}:${config.imap_port}`);
  console.log(`📤 SMTP: ${config.smtp_server}:${config.smtp_port}`);
  console.log(`\n🔒 配置文件权限已设置为 600（仅所有者可读写）`);
  console.log('\n运行以下命令测试连接：');
  console.log(`  node scripts/test-connection.js\n`);

  rl.close();
}

init().catch(console.error);
