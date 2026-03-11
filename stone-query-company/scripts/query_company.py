#!/usr/bin/env python3
"""
企业工商信息查询脚本
通过阿里云 API 市场查询企业工商注册信息
"""

import urllib.request
import urllib.parse
import ssl
import json
import sys


def get_company_info(company_name, appcode=None):
    """
    查询企业工商信息

    Args:
        company_name: 企业名称、注册号、统一信用代码、组织机构代码
        appcode: 阿里云 API AppCode（可选，默认使用内置配置）

    Returns:
        dict: 包含查询结果或错误信息的字典
    """
    host = 'https://cardnotwo.market.alicloudapi.com'
    path = '/companyQuery'

    # 如果没有提供 appcode，使用默认配置
    if appcode is None:
        # 注意：实际使用时请替换为您的真实 AppCode
        appcode = 'YOUR_APPCODE_HERE'

    url = host + path

    bodys = {
        'com': company_name,
        'X_Ca_Error_Code': 'NO'
    }
    post_data = urllib.parse.urlencode(bodys).encode('utf-8')
    request = urllib.request.Request(url, data=post_data)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        response = urllib.request.urlopen(request, context=ctx)
        content = response.read().decode('utf-8')

        if response.getcode() == 200:
            result = json.loads(content)
            error_code = result.get('error_code')

            if error_code == 0:
                # 提取 result 字段中的数据
                data = result.get('result', {})

                # 组装返回信息
                formatted_info = {
                    'success': True,
                    'companyName': data.get('companyName', '无'),
                    'companyNameold': data.get('companyNameold', '无'),
                    'creditCode': data.get('creditCode', '无'),
                    'companyCode': data.get('companyCode', '无'),
                    'regNumber': data.get('regNumber', '无'),
                    'taxNumber': data.get('taxNumber', '无'),
                    'regType': data.get('regType', '无'),
                    'faRen': data.get('faRen', '无'),
                    'issueTime': data.get('issueTime', '无'),
                    'chkDate': data.get('chkDate', '无'),
                    'bussiness': data.get('bussiness', '无'),
                    'cancelDate': data.get('cancelDate', '无'),
                    'regMoney': data.get('regMoney', '无'),
                    'address': data.get('address', '无'),
                    'industry': data.get('industry', '无'),
                    'industryCategory': data.get('industryCategory', '无')
                }
                return formatted_info
            elif error_code == 50002:
                return {
                    'success': False,
                    'error': '根据提供的企业名称，未查询到企业工商信息，请进一步核实企业名称是否准确'
                }
            else:
                return {
                    'success': False,
                    'error': f'获取企业工商信息失败，错误码: {error_code}'
                }
        else:
            return {
                'success': False,
                'error': f'HTTP请求失败，状态码: {response.getcode()}'
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'请求异常: {str(e)}'
        }


def format_company_info(data):
    """格式化企业信息为易读文本"""
    if not data.get('success'):
        return data.get('error', '查询失败')

    return f"""企业工商信息查询结果：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 基本信息
  公司名称：{data.get('companyName', '无')}
  历史名称：{data.get('companyNameold', '无')}
  公司类型：{data.get('regType', '无')}

🔢 代码信息
  统一信用代码：{data.get('creditCode', '无')}
  组织机构代码：{data.get('companyCode', '无')}
  注册号：{data.get('regNumber', '无')}
  税号：{data.get('taxNumber', '无')}

👤 法人信息
  法定代表人：{data.get('faRen', '无')}

📅 时间信息
  成立时间：{data.get('issueTime', '无')}
  核准时间：{data.get('chkDate', '无')}
  营业期限：{data.get('bussiness', '无')}
  注销时间：{data.get('cancelDate', '无')}

💰 资本信息
  注册资本：{data.get('regMoney', '无')}

📍 地址与行业
  注册地址：{data.get('address', '无')}
  所属行业：{data.get('industry', '无')}
  行业分类：{data.get('industryCategory', '无')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python query_company.py <企业名称>", file=sys.stderr)
        print("示例: python query_company.py '北京百度网讯科技有限公司'", file=sys.stderr)
        sys.exit(1)

    company_name = sys.argv[1]

    # 支持从环境变量读取 AppCode
    import os
    appcode = os.environ.get('COMPANY_QUERY_APPCODE', 'YOUR_APPCODE_HERE')

    result = get_company_info(company_name, appcode)

    # 输出 JSON 格式结果（便于程序解析）
    print(json.dumps(result, ensure_ascii=False, indent=2))
