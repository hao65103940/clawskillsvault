#!/usr/bin/env node
/**
 * 测试邮箱连接
 * 用法：node scripts/test-connection.js
 */

const fs = require('fs');
const path = require('path');
const imaplib = require('imap');
const { SimpleSMTPClient } = require('smtp-client');

const CONFIG_PATH = path.join(__dirname, '../config.json');

async function testIMAP(config) {
  console.log(`\n📥 测试 IMAP 连接 (${config.imap_server}:${config.imap_port})...`);
  
  return new Promise((resolve, reject) => {
    const ImapClient = require('imap');
    const imap = new ImapClient({
      user: config.email,
      password: config.password,
      host: config.imap_server,
      port: config.imap_port,
      tls: true,
      tlsOptions: { rejectUnauthorized: false }
    });

    imap.once('ready', () => {
      console.log('✅ IMAP 连接成功！');
      imap.end();
      resolve(true);
    });

    imap.once('error', (err) => {
      console.log(`❌ IMAP 连接失败：${err.message}`);
      reject(err);
    });

    imap.connect();
    
    setTimeout(() => {
      imap.end();
      reject(new Error('连接超时'));
    }, 10000);
  });
}

async function testSMTP(config) {
  console.log(`\n📤 测试 SMTP 连接 (${config.smtp_server}:${config.smtp_port})...`);
  
  return new Promise((resolve, reject) => {
    const SMTPConnection = require('smtp-connection');
    const client = new SMTPConnection({
      host: config.smtp_server,
      port: config.smtp_port,
      secure: false,
      requireTLS: true,
      auth: {
        user: config.email,
        pass: config.password
      }
    });

    client.connect();

    client.once('connect', () => {
      console.log('✅ SMTP 连接成功！');
      client.quit();
      resolve(true);
    });

    client.once('error', (err) => {
      console.log(`❌ SMTP 连接失败：${err.message}`);
      reject(err);
    });

    setTimeout(() => {
      client.quit();
      reject(new Error('连接超时'));
    }, 10000);
  });
}

async function main() {
  console.log('📧 邮箱连接测试\n');

  // 检查配置
  if (!fs.existsSync(CONFIG_PATH)) {
    console.log('❌ 配置文件不存在！');
    console.log('请先运行初始化：node scripts/init.js\n');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  
  console.log(`📧 邮箱：${config.email}`);
  console.log(`🏢 服务商：${config.provider || 'unknown'}`);

  try {
    await testIMAP(config);
  } catch (e) {
    console.log('💡 提示：检查授权码是否正确，或联系邮箱管理员开启 IMAP 服务');
  }

  try {
    await testSMTP(config);
  } catch (e) {
    console.log('💡 提示：检查授权码是否正确，或联系邮箱管理员开启 SMTP 服务');
  }

  console.log('\n✅ 连接测试完成！\n');
}

main().catch(console.error);
