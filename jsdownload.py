import os
import requests
import argparse
import urllib3
import ast
import json
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LegacySSLAdapter(HTTPAdapter):
    """解决老旧SSL/TLS协议兼容性问题"""
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

def parse_js_dict(input_str):
    """
    解析输入字符串为字典格式
    支持两种格式：
    1. Python字典格式：{3:"264be3e",4:"619f1fb"}
    2. JSON格式：{"3":"264be3e","4":"619f1fb"}
    """
    try:
        # 尝试解析为Python字典
        js_dict = ast.literal_eval(input_str)
    except (SyntaxError, ValueError):
        try:
            # 如果不是Python字典格式，尝试解析为JSON
            js_dict = json.loads(input_str)
        except json.JSONDecodeError:
            print("无法解析输入格式，请确保格式正确")
            return {}
    
    # 确保所有键和值都转换为字符串
    return {str(key): str(value) for key, value in js_dict.items()}

def download_js_files(js_dict, base_url, folder='outjs-xxx', proxies=None, insecure=False):
    if not os.path.exists(folder):
        os.makedirs(folder)

    session = requests.Session()
    
    # 添加SSL兼容性适配器
    if insecure:
        session.mount('https://', LegacySSLAdapter())
    
    for key, value in js_dict.items():
        # 生成JS文件名：key.value.js
        js_filename = f"{key}.{value}.js"
        
        file_path, file_name = os.path.split(js_filename)
        full_file_path = os.path.join(folder, file_path)

        if not os.path.exists(full_file_path):
            os.makedirs(full_file_path)

        js_url = base_url + '/' + js_filename
        js_filepath = os.path.join(full_file_path, file_name)
        
        try:
            download_file(session, js_url, js_filepath, proxies=proxies, insecure=insecure)
            print(f'Downloaded {js_url} to {js_filepath}')
        except Exception as e:
            print(f'Failed to download {js_url}: {str(e)}')

def download_file(session, url, filename, proxies=None, insecure=False):
    response = session.get(
        url, 
        proxies=proxies,
        verify=not insecure,  # 禁用SSL验证
        timeout=30
    )
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='下载JS文件工具')
    parser.add_argument('--proxy', type=str, help='SOCKS代理地址 (e.g. socks5://127.0.0.1:1080)')
    parser.add_argument('--insecure', action='store_true', help='禁用SSL验证，解决老旧协议兼容性问题')
    args = parser.parse_args()

    proxies = {'http': args.proxy, 'https': args.proxy} if args.proxy else None
    base_url = 'https://xxxxx/static/js'
    
    # 读取并解析js.txt文件
    with open('js.txt', 'r') as file:
        js_file_content = file.read().strip()
    
    # 解析为字典格式
    js_dict = parse_js_dict(js_file_content)
    
    if not js_dict:
        print("错误：无法解析js.txt中的内容")
        exit(1)
    
    print(f"成功解析 {len(js_dict)} 个JS文件")
    
    download_js_files(
        js_dict, 
        base_url, 
        proxies=proxies, 
        insecure=args.insecure
    )