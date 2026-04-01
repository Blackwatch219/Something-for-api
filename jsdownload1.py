import os
import requests
import argparse
import urllib3
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

def download_js_files(js_file_names, base_url, folder='out-h5', proxies=None, insecure=False):
    if not os.path.exists(folder):
        os.makedirs(folder)

    session = requests.Session()
    
    # 添加SSL兼容性适配器
    if insecure:
        session.mount('https://', LegacySSLAdapter())
    
    for js_filename in js_file_names:
        if not js_filename.endswith('.js'):
            print(f'Skipping non-JavaScript file: {js_filename}')
            continue

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
    base_url = 'https://h5.gateway.zjcloud.com:50456/assets'
    
    with open('js.txt', 'r') as file:
        js_file_names = file.read().splitlines()

    download_js_files(
        js_file_names, 
        base_url, 
        proxies=proxies, 
        insecure=args.insecure
    )