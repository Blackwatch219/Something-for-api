import os
import re
import pandas as pd

import re
import os

def extract_paths_from_js_files(directory):
    # 专门匹配JS文件中路径的正则表达式
    path_pattern = re.compile(
        r"""
        (?:['"`])                     # 匹配引号开头（单引号、双引号或反引号）
        (                             # 捕获组开始
            (?:                        # 匹配路径模式：
                \.\.?\/[\w\-\.\/]*     # 相对路径：../ 或 ./
                | \/[\w\-\.\/]+        # 绝对路径：/开头
                | [\w\-]+\.(?:js|css|png|jpg|svg|json|html?)  # 文件扩展名
                | [\w\-]+\/[\w\-\.]+   # 目录/文件格式
            )
        )                             # 捕获组结束
        (?:['"`])                     # 匹配引号结尾
        """,
        re.VERBOSE
    )
    
    paths = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        found_paths = path_pattern.findall(content)
                        for path in found_paths:
                            # 去重并添加
                            if path not in paths:
                                paths.append((path, file_path))
                except Exception as e:
                    print(f"读取文件 {file_path} 时发生错误: {e}")
    
    return paths


if __name__ == '__main__':
    directory = input('请输入要扫描的目录：')
    output_file = input('请输入输出Excel文件的路径：')

    endpoints = extract_paths_from_js_files(directory)

    # 创建DataFrame
    df = pd.DataFrame(endpoints, columns=['API Endpoint', 'Source JS File'])

    try:
        # 保存到Excel文件
        df.to_excel(output_file, index=False)
        print(f'提取到的API端点已保存到Excel文件：{output_file}')
    except Exception as e:
        print(f'写入Excel文件 {output_file} 时发生错误: {e}')