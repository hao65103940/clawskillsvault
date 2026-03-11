#!/usr/bin/env python3
"""
腾讯企业邮完整工具 - 支持收发邮件 + 附件
用法：
  python email_tool.py send --to xxx@xxx.com --subject "主题" --text "内容" --attach file.pdf
  python email_tool.py read --limit 10
  python email_tool.py read --uid 123 --full
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
import os
import json
import argparse
import base64
import re
from datetime import datetime

# 加载配置
def load_config():
    """加载配置文件"""
    config_paths = [
        os.path.join(os.path.dirname(__file__), 'config.json'),
        os.path.expanduser('~/.stone-email/config.json'),
        os.path.join(os.getcwd(), 'config.json')
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # 默认配置（腾讯企业邮示例）
    return {
        "email": "your-email@example.com",
        "password": "your-auth-code",
        "imap_server": "imap.exmail.qq.com",
        "imap_port": 993,
        "smtp_server": "smtp.exmail.qq.com",
        "smtp_port": 587,
        "provider": "tencent"
    }

# 初始化配置
CONFIG = load_config()
EMAIL = CONFIG.get("email", "")
PASSWORD = CONFIG.get("password", "")
IMAP_SERVER = CONFIG.get("imap_server", "imap.exmail.qq.com")
IMAP_PORT = CONFIG.get("imap_port", 993)
SMTP_SERVER = CONFIG.get("smtp_server", "smtp.exmail.qq.com")
SMTP_PORT = CONFIG.get("smtp_port", 587)

def render_template(template_path, variables):
    """渲染 HTML 模板"""
    if not os.path.exists(template_path):
        return None
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单变量替换
    for key, value in variables.items():
        content = content.replace(f'{{{{{key}}}}}', str(value) if value else '')
    
    # 条件渲染
    # 处理 {{#if variable}}...{{/if}}
    if_pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
    def replace_if(match):
        var_name = match.group(1)
        if_content = match.group(2)
        return if_content if variables.get(var_name) else ''
    content = re.sub(if_pattern, replace_if, content, flags=re.DOTALL)
    
    return content

def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ""
    decoded = []
    for part, encoding in decode_header(s):
        if isinstance(part, bytes):
            try:
                decoded.append(part.decode(encoding or 'utf-8', errors='replace'))
            except:
                decoded.append(part.decode('latin-1', errors='replace'))
        else:
            decoded.append(part)
    return ''.join(decoded)

def read_emails(limit=10, full=False, uid=None):
    """读取邮件"""
    try:
        # 连接 IMAP 服务器
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')
        
        if uid:
            # 读取指定邮件
            status, msg_data = mail.fetch(str(uid), '(RFC822)')
            if status != 'OK':
                print(f"❌ 获取邮件失败：{msg_data}")
                return []
            messages = [msg_data[0][1]]
        else:
            # 获取最新邮件
            status, data = mail.search(None, 'ALL')
            if status != 'OK':
                print("❌ 搜索邮件失败")
                return []
            
            msg_ids = data[0].split()
            messages = []
            for msg_id in msg_ids[-limit:]:
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status == 'OK':
                    messages.append(msg_data[0][1])
        
        # 解析邮件
        emails_list = []
        for msg_bytes in messages:
            msg = email.message_from_bytes(msg_bytes)
            
            # 提取发件人
            from_ = decode_mime_words(msg.get('From', ''))
            
            # 提取主题
            subject = decode_mime_words(msg.get('Subject', ''))
            
            # 提取日期
            date = msg.get('Date', '')
            
            # 提取正文
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition") or "")
                    
                    # 跳过附件
                    if "attachment" in content_disposition:
                        continue
                    
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                            break
                        except:
                            pass
                    elif content_type == "text/html" and not body:
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    body = "无法解析正文"
            
            # 提取附件信息
            attachments = []
            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = str(part.get("Content-Disposition") or "")
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            filename = decode_mime_words(filename)
                            attachments.append({
                                "filename": filename,
                                "content_type": part.get_content_type()
                            })
            
            email_data = {
                "from": from_,
                "subject": subject,
                "date": date,
                "body": body if full or len(body) < 500 else body[:500] + "...",
                "attachments": attachments
            }
            
            # 获取 UID
            if not uid:
                status, uid_data = mail.fetch(msg_ids[-len(messages) + len(emails_list)], '(UID)')
                if status == 'OK':
                    uid_str = uid_data[0].decode()
                    uid_val = uid_str.split('UID')[1].strip() if 'UID' in uid_str else ''
                    email_data['uid'] = uid_val
            
            emails_list.append(email_data)
        
        mail.close()
        mail.logout()
        
        return emails_list
    
    except Exception as e:
        print(f"❌ 读取邮件失败：{e}")
        return []

def send_email(to_emails, subject, text, html=None, cc_emails=None, bcc_emails=None, attachments=None):
    """发送邮件 - 支持多收件人、抄送、密送"""
    try:
        # 处理收件人列表
        if isinstance(to_emails, str):
            to_emails = [to_emails]
        to_list = [e.strip() for e in to_emails if e.strip()]
        
        # 处理抄送列表
        cc_list = []
        if cc_emails:
            if isinstance(cc_emails, str):
                cc_emails = [cc_emails]
            cc_list = [e.strip() for e in cc_emails if e.strip()]
        
        # 处理密送列表
        bcc_list = []
        if bcc_emails:
            if isinstance(bcc_emails, str):
                bcc_emails = [bcc_emails]
            bcc_list = [e.strip() for e in bcc_emails if e.strip()]
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = ', '.join(to_list)
        msg['Subject'] = subject
        
        # 添加抄送
        if cc_list:
            msg['Cc'] = ', '.join(cc_list)
        
        # 添加正文（同时支持纯文本和 HTML）
        if html and text:
            # 多部分正文
            msg_alternative = MIMEMultipart('alternative')
            msg_alternative.attach(MIMEText(text, 'plain', 'utf-8'))
            msg_alternative.attach(MIMEText(html, 'html', 'utf-8'))
            msg.attach(msg_alternative)
        elif html:
            msg.attach(MIMEText(html, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText(text, 'plain', 'utf-8'))
        
        # 添加附件
        attached_files = []
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        filename = os.path.basename(file_path)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="{filename}"'
                        )
                        msg.attach(part)
                        attached_files.append(filename)
                        print(f"  📎 附件：{filename}")
        
        # 获取所有收件人（包括密送）
        all_recipients = to_list + cc_list + bcc_list
        
        # 发送邮件
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, all_recipients, msg.as_string())
        server.quit()
        
        return {
            "success": True,
            "to": to_list,
            "cc": cc_list,
            "bcc": bcc_list,
            "subject": subject,
            "attachments": attached_files
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def list_attachments(uid):
    """列出指定邮件的附件"""
    emails = read_emails(uid=uid, full=True)
    if emails and emails[0].get('attachments'):
        print(f"📎 邮件附件 ({len(emails[0]['attachments'])} 个):")
        for att in emails[0]['attachments']:
            print(f"  - {att['filename']} ({att['content_type']})")
    else:
        print("❌ 无附件或邮件不存在")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='腾讯企业邮工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 读取邮件
    read_parser = subparsers.add_parser('read', help='读取邮件')
    read_parser.add_argument('--limit', type=int, default=10, help='读取数量')
    read_parser.add_argument('--uid', type=str, help='指定邮件 UID')
    read_parser.add_argument('--full', action='store_true', help='显示完整正文')
    read_parser.add_argument('--attachments', action='store_true', help='列出附件')
    
    # 发送邮件
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('--to', required=True, nargs='+', help='收件人（支持多个）')
    send_parser.add_argument('--cc', nargs='+', help='抄送人（支持多个）')
    send_parser.add_argument('--bcc', nargs='+', help='密送人（支持多个）')
    send_parser.add_argument('--subject', required=True, help='主题')
    send_parser.add_argument('--text', default='', help='正文')
    send_parser.add_argument('--html', default='', help='HTML 正文')
    send_parser.add_argument('--template', default='', help='HTML 模板文件路径')
    send_parser.add_argument('--var', nargs='*', help='模板变量 (格式：key=value)')
    send_parser.add_argument('--attach', nargs='*', help='附件路径')
    
    args = parser.parse_args()
    
    if args.command == 'read':
        if args.attachments and args.uid:
            list_attachments(args.uid)
        else:
            emails = read_emails(limit=args.limit, full=args.full, uid=args.uid)
            if emails:
                print(f"📧 找到 {len(emails)} 封邮件:\n")
                for i, e in enumerate(emails, 1):
                    print(f"{i}. 来自：{e['from']}")
                    print(f"   主题：{e['subject']}")
                    print(f"   日期：{e['date']}")
                    if e.get('uid'):
                        print(f"   UID: {e['uid']}")
                    if e['attachments']:
                        print(f"   📎 附件：{len(e['attachments'])} 个")
                    print(f"   正文：{e['body'][:200]}...")
                    print()
            else:
                print("❌ 无邮件")
    
    elif args.command == 'send':
        print(f"📤 发送邮件")
        print(f"   收件人：{', '.join(args.to)}")
        if args.cc:
            print(f"   抄送：{', '.join(args.cc)}")
        if args.bcc:
            print(f"   密送：{', '.join(args.bcc)}")
        print(f"   主题：{args.subject}")
        
        # 读取 HTML 模板
        html_content = args.html
        if args.template and os.path.exists(args.template):
            # 准备模板变量
            template_vars = {
                'subject': args.subject,
                'greeting': '你好，',
                'content': args.text,
                'sender_name': 'AI 助手',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'button': '',
                'button_text': '',
                'button_link': '',
                'highlight': ''
            }
            
            # 解析 --var 参数
            if hasattr(args, 'var') and args.var:
                for var in args.var:
                    if '=' in var:
                        key, value = var.split('=', 1)
                        template_vars[key.strip()] = value.strip()
            
            html_content = render_template(args.template, template_vars)
            print(f"   模板：{args.template}")
        
        result = send_email(args.to, args.subject, args.text, html_content, args.cc, args.bcc, args.attach)
        if result['success']:
            print(f"✅ 发送成功！")
            if result.get('cc'):
                print(f"   抄送：{len(result['cc'])} 人")
            if result.get('bcc'):
                print(f"   密送：{len(result['bcc'])} 人")
            if result.get('attachments'):
                print(f"   附件：{len(result['attachments'])} 个 - {', '.join(result['attachments'])}")
        else:
            print(f"❌ 发送失败：{result.get('error')}")
    
    else:
        parser.print_help()
